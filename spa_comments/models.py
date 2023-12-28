import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from collections import deque


class Author(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )

    def __str__(self):
        return self.username


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="comments")
    published_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(validators=[MinLengthValidator(1)])

    class Meta:
        ordering = ['-published_at']

    def clean(self):
        super().clean()

        allowed_tags = (
            "<a>", "</a>", "<code>", "</code>", "<i>", "</i>", "<strong>", "</strong>"
        )

        tags_deque = deque()

        tags = re.findall(r"<[^>]*>", self.text)

        for tag in tags:
            if "/" not in tag:
                if tag.startswith("<a "):
                    tag = tag.split()[0] + ">"
                tags_deque.append(tag)
            else:
                if not tags_deque:
                    raise ValidationError("Closed tags must match opening tags!")

                if tag not in allowed_tags:
                    raise ValidationError(
                        "Unsupported HTML tag used! Only following HTML tags are allowed: "
                        "<a></a>, <code></code>, <i></i>, <strong></strong>"
                    )

                opening_tag = tags_deque.pop()
                if opening_tag[1:] != tag[2:]:
                    raise ValidationError("Opening tags must match closing tags!")

        if len(tags_deque) != 0:
            raise ValidationError("All opened HTML tags must be closed!")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        formatted_time = self.published_at.strftime("%H:%M:%S %d-%m-%Y")
        return f"Comment by {self.author} at {formatted_time}"


class Reply(models.Model):
    original_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    reply = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="original_comment")
