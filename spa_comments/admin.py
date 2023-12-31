from django.contrib import admin
from django.contrib.auth.models import Group

from spa_comments.models import Comment, Author


admin.site.register(Author)
admin.site.register(Comment)

admin.site.unregister(Group)
