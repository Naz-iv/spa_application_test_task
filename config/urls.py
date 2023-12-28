from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("spa_comments.urls", namespace="spa-comments")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path('captcha/', include('captcha.urls')),

]
