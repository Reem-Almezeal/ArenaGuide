import re
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "form-control"
        })
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm Password",
            "class": "form-control"
        })
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone", "password"]
        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Username",
                "class": "form-control"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Email",
                "class": "form-control"
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "05XXXXXXXX",
                "class": "form-control"
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if not email:
            raise forms.ValidationError("Email is required.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")

        if phone:
            if not re.match(r"^05\d{8}$", phone):
                raise forms.ValidationError("Enter a valid Saudi phone number, like 05XXXXXXXX.")

            if User.objects.filter(phone=phone).exists():
                raise forms.ValidationError("Phone number already exists.")

        return phone

    def clean_password(self):
        password = self.cleaned_data.get("password")
        validate_password(password)
        return password

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "form-control"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "form-control"
        })
    )