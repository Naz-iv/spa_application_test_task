import random
import string

from django.core.cache import cache

from spa_comments.models import Comment


def generate_random_alphanumeric_challenge(length=6):
    challenge = u""
    response = u""
    characters = string.ascii_uppercase + string.digits

    for _ in range(length):
        digit = random.choice(characters)
        challenge += digit
        response += digit

    return challenge, response


def get_expensive_data():
    """Reads all comments from Database and saves them to cache"""

    data = cache.get("comments_cache")

    if data is None:
        data = Comment.objects.filter(parent_comment__isnull=False)

        cache.set("comments_cache", data, timeout=3600)

    return data
