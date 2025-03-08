from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    skills = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    location = forms.CharField(max_length=255, required=False)
    preferred_roles = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                skills=self.cleaned_data['skills'],
                location=self.cleaned_data['location'],
                preferred_roles=self.cleaned_data['preferred_roles']
            )
        return user