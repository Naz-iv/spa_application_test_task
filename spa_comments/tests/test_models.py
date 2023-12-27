from django.contrib.auth import get_user_model
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
            text="This is <strong>test</strong> text without any HTML tags!"
                 "<a href='#' title='Test'>Test link</a>' <i>Test</i>"
                 "<code>Test information in code tag</code>"
        )
        self.assertEqual(
            comment,
            Comment.objects.get(id=comment.id)
        )

    def test_comment_validation_with_invalid_tags(self):
        pass
