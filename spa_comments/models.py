import os
import re
import uuid

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, FileExtensionValidator
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


def create_path_for_image(instance, filename: str):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads/images/",
        f"image-{uuid.uuid4()}{extension}"
    )


def create_path_for_file(instance, filename: str):
    _, extension = os.path.splitext(filename)
    return os.path.join(
        "uploads/files/",
        f"file-{uuid.uuid4()}{extension}"
    )

def validate_file_size(file):
    max_size = 100 * 1024
    if file.size > max_size:
        raise ValidationError("File size must be less than 100 KB.")


class Comment(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="comments")
    published_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(validators=[MinLengthValidator(1)])
    parent_comment = models.ForeignKey(
        "Comment", on_delete=models.SET_NULL, null=True, blank=True, related_name="replies"
    )
    image = models.ImageField(
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "gif", "png"])],
        upload_to=create_path_for_image
    )
    file = models.FileField(
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["txt"]), validate_file_size],
        upload_to=create_path_for_file
    )

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

        if self.image:
            img = Image.open(self.image.path)
            max_size = (320, 240)
            img.thumbnail(max_size)
            img.save(self.image.path)

    def __str__(self):
        formatted_time = self.published_at.strftime("%H:%M:%S %d-%m-%Y")
        return f"Comment by {self.author} at {formatted_time}"
