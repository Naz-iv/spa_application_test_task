from django.urls import path

from spa_comments.views import (
    index,
    login,
    logout,
    CommentCreateView,
    CommentListView, signup
)

urlpatterns = [
    path("", index, name="home"),
    path("comments/create/", CommentCreateView.as_view(), name="comment-create"),
    path("comments/", CommentListView.as_view(), name="comment-list"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),

]

app_name = "spa-comments"
