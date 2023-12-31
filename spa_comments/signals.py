from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

from spa_comments.models import Comment


@receiver(post_save, sender=Comment)
def update_cache_on_model_save(sender, instance, **kwargs):
    """Function to invalidate cached comments on new comment creation"""
    cache.delete("comments_cache")
