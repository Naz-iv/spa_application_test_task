from django.urls import path

from spa_comments.views import (
    index,
    CommentCreateView,
    CommentListView
)

urlpatterns = [
    path("", index, name="home"),
    path("comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/", CommentListView.as_view(), name="comment-list"),
    path("comments/my/", CommentListView.as_view(), name="comment-my"),
]

app_name = "spa-comments"
