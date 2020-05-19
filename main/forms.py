from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        permissions = (("not_admin"))
        model = User
        fields = ["username", "email", "password",] 

    """def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.number = self.cleaned_data["number"]
        if commit:
            user.save()
        return user   """

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['num',]     