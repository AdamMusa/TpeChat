from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=255)
    email = forms.EmailField()
    password1 = forms.CharField(
        label='Mot de passe', 
        widget=forms.PasswordInput(attrs={'icon': 'ti-lock'}),
        help_text = 'Au moins 8 caractères, pas uniquement des chiffres',

    )
    password2 = forms.CharField(
        label='Mot de passe confirmation', 
        widget=forms.PasswordInput(attrs={'icon': 'ti-lock'})
    )
   
    class Meta:
        model = User
        fields = ('username','email' )
        widgets = {
            'email': forms.EmailInput(attrs={'icon': 'ti-email'})
        }
   

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']