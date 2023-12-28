from django.urls import path, include

from accounts.views import custom_login, signup


urlpatterns = [
    path("login/", custom_login, name="login"),
    path("signup/", signup, name="signup"),
    path("", include("django.contrib.auth.urls")),
]

app_name = "accounts"
