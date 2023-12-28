from captcha.fields import CaptchaField
from django import forms

from spa_comments.models import Comment, Reply


class CommentCreateForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your username..."}),
        required=True,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email..."}),
        required=True,
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "textarea", "placeholder": "Enter your comment..."}),
        required=True,
    )

    captcha = CaptchaField(
        label="Captcha",
        help_text="Enter the captcha"
    )

    class Meta:
        model = Comment
        fields = ["username", "email", "text", "captcha"]


class ReplyCreateForm(forms.ModelForm):
    original_comment_id = forms.IntegerField(
        label="Comment ID",
        widget=forms.HiddenInput()
    )
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your username..."}),
        required=True,
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email..."}),
        required=True,
    )

    text = forms.CharField(
        widget=forms.Textarea(attrs={"class": "textarea", "placeholder": "Enter your comment..."}),
        required=True,
    )

    captcha = CaptchaField(
        label="Captcha",
        help_text="Enter the captcha"
    )

    class Meta:
        model = Reply
        fields = ["username", "email", "text", "captcha", "original_comment_id"]
