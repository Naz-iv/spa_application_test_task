from django import template
from django.db.models import QuerySet

from spa_comments.models import Comment

register = template.Library()


@register.simple_tag()
def get_reply_list(comment: Comment, comments_cache: list[Comment]) -> list[Comment]:
    """
    Links reply comments to its parent comment without additional requests to database
    :param comment: parent reply object
    :param comments_cache: list of comments from database cached to context variable to avoid additional requests to database
    :return: list of replies of a given comment
    """
    return [item for item in comments_cache if item.parent_comment_id == comment.id]
