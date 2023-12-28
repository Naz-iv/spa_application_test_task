from django.urls import path

from spa_comments.views import (
    CommentCreateView,
    CommentListView, ReplyCreateView
)

urlpatterns = [
    path("", CommentListView.as_view(), name="home"),
    path("comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/my/", CommentListView.as_view(), name="comment-my"),
    path("comments/<int:pk>/reply/", ReplyCreateView.as_view(), name="reply-create"),

]

app_name = "spa-comments"
