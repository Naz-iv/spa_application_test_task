from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from spa_comments.models import Comment


class ModelTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            email="test_email@email.com",
            password="StrongPassword"
        )
        self.comment = Comment.objects.create(
            user_id=self.user.id,
            published_at=timezone.now(),
            text="This is test text without any HTML tags!"
        )

    def test_comment_validation_without_tags(self):
        self.assertEqual(
            self.comment,
            Comment.objects.get(id=self.comment.id)
        )

    def test_comment_validation_with_valid_tags(self):
        comment = Comment.objects.create(
            user_id=1,
            published_at=timezone.now(),
            text="This is <strong>test</strong> text with all HTML tags!"
                 "<a href='#' title='Test'>Test link</a>' <i>Test</i>"
                 "<code>Test information in code tag</code>"
        )
        self.assertEqual(
            comment,
            Comment.objects.get(id=comment.id)
        )

    def test_comment_validation_with_invalid_tags(self):
        with self.assertRaises(ValidationError):
            Comment.objects.create(
                user_id=1,
                published_at=timezone.now(),
                text="This is <h1>test</h1> text with wrong HTML tags!"
                     "<a href='#' title='Test'>Test link</a>' <i>Test</i>"
                     "<div>Test information in code tag</div>"
            )

    def test_comment_validation_with_tag_not_closed(self):
        with self.assertRaises(ValidationError):
            Comment.objects.create(
                user_id=1,
                published_at=timezone.now(),
                text="This is <strong>test</strong> text with all HTML tags!"
                     "<a href='#' title='Test'>Test link</a>' <i>Test</i>"
                     "<code>Test information in code tag."
            )

    def test_user_str_method(self):
        self.assertEqual(
            self.user.username,
            str(self.user)
        )

    def test_comment_str_method(self):
        formatted_time = self.comment.published_at.strftime("%H:%M:%S %d-%m-%Y")

        self.assertEqual(
            str(self.comment),
            f"Comment by {self.comment.user} at {formatted_time}"
        )
