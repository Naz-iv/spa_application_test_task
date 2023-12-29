from captcha.fields import CaptchaField
from django import forms

from spa_comments.models import Comment


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
    image = forms.ImageField(
        label="Image",
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload image..."}),
        required=False,
    )
    file = forms.FileField(
        label="File",
        widget=forms.FileInput(attrs={"class": "form-control", "placeholder": "Upload file...", "accept": ".txt"}),
        required=False,
    )
    parent_comment_id = forms.IntegerField(
        label="Parent ID",
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Comment
        fields = ["username", "email", "text", "captcha", "image", "file", "parent_comment_id"]
