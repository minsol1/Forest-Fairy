from django import forms
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, UserCreationForm, UsernameField, UserChangeForm, PasswordChangeForm
from django.utils import timezone

class UserForm(UserCreationForm):
    year = timezone.now().year
    years = [x for x in range(1970, year + 1)]
    username = UsernameField(
        label='',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': '아이디',
            'class': 'register_idForm'
        }))
    password1 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': '비밀번호',
            'class': 'register_pwForm'
        }))
    password2 = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={
            'placeholder': '비밀번호 확인',
            'class': 'register_pwcheckForm'
        }))
    email = forms.EmailField(
        label='',
        widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'register_emailForm'}))
    nickname = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'placeholder': '닉네임', 'class': 'register_nicknameForm'}))
    birthdate = forms.DateField(label='생년월일',
                                widget=forms.SelectDateWidget(
                                    years=years,
                                    attrs={
                                        'class': 'register_birthForm col-3',
                                        'default': 1990
                                    }))
    gender = forms.ChoiceField(
        label='성별',
        choices=User.GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'register_genderForm'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'username', 'password1', 'password2', 'nickname', 'email',
            'birthdate', 'gender',
        ]


