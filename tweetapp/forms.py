from django import forms
from . models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            user.profile.avatar = self.cleaned_data['avatar']
            user.profile.save()
        return user

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',  # Bootstrap class for consistent styling
                'rows': 3,  # Set the number of rows to 3
                'placeholder': 'Write your tweet here...',
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
        }



