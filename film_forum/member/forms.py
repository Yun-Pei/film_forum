from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget= forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )


class RegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )
    # img = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control"
    #         }
    #     )
    # )
    img = forms.CharField(
        widget=forms.HiddenInput(),  # 使用 HiddenInput widget
        required=False,  # 如果前端不提供此字段，則不會引發錯誤
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'img')
# , 'img'
