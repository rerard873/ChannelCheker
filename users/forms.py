from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError

from users.models import User


class UserAuthForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder' : 'Введите логин' }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    class Meta:
        model = User
        fields = ['username','password']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите логин'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Введите почту'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Такой email уже используется")
        return email


class AvatarChangeForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class':'avatar-preview'}))
    class Meta:
        model = User
        fields =['avatar']

