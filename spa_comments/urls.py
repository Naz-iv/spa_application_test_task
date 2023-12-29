from django.urls import path

from spa_comments.views import (
    CommentCreateView,
    CommentListView,
)

urlpatterns = [
    path("", CommentListView.as_view(), name="home"),
    path("comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/<int:pk>/reply/", CommentCreateView.as_view(), name="comment-reply"),
    path("comments/my/", CommentListView.as_view(), name="comment-my"),

]

app_name = "spa-comments"
