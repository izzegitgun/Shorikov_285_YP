from django import forms
from allauth.account.forms import SignupForm

from .models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class CustomSignupForm(SignupForm):
    ROLE_CHOICES = [
        ("teacher", "Преподаватель"),
        ("curator", "Куратор"),
        ("accountant", "Бухгалтер"),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label="Роль в системе",
        help_text="Выберите вашу роль: преподаватель, куратор или бухгалтер.",
    )

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data.get("role", User.Roles.TEACHER)
        user.save()
        return user


class UserManageForm(forms.ModelForm):
    new_password = forms.CharField(
        label="Новый пароль",
        required=False,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Оставьте пустым, если не нужно менять пароль",
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "role", "is_active"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


