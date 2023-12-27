import re

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from collections import deque


class User(AbstractUser):
    email = models.EmailField()
    profile_image = models.ImageField(null=True, blank=True)


def validate_text(text: str) -> str:
    """Validates that all HTML tags were closed correctly and permitted HTML tags used"""
    print("validating text")
    allowed_tags = ("a", "code", "i", "strong")

    tags_deque = deque()

    tags = re.findall(r"<[^>]*>", text)

    for tag in tags:
        print("Tag:", tag)
        if "/" not in tag:
            if tag.split().strip("<").strip(">")[0] not in allowed_tags:
                raise ValidationError(
                    "Unsupported HTML tag used! Only following HTML tags are allowed: "
                    "<a></a>, <code></code>, <i></i>, <strong></strong>"
                )
            tags_deque.append(tag)
        else:
            if not tags_deque:
                raise ValidationError("Closed tags must match opening tags!")
            opening_tag = tags_deque.pop()
            if opening_tag[1:] != tag[2:-1]:
                raise ValidationError("Opening tags must match closing tags!")

    if len(tags_deque) != 0:
        raise ValidationError("All opened HTML tags must be closed!")

    return text


class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments")
    published_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(validators=[MinLengthValidator(1), validate_text])

    class Meta:
        ordering = ['-published_at']


class Reply(models.Model):
    original_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    reply = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="original_comment")
