from django import forms
from django.contrib.auth.password_validation import MinimumLengthValidator, CommonPasswordValidator


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email...'}),
        required=True,
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password...'}),
        required=True,
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username...'}),
        required=True,
    )
    email = forms.EmailField(
        label='Email address',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email...'}),
        required=True,
    )

    password1 = forms.CharField(
        label='Password',

        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password...'}),
        required=True,
        validators=[MinimumLengthValidator(8), CommonPasswordValidator()],
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your password...'}),
        required=True,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

