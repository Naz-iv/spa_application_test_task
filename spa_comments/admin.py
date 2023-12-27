from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from spa_comments.models import Comment, Reply, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


admin.site.register(Comment)
admin.site.register(Reply)

admin.site.unregister(Group)
