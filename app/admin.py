from django.contrib import admin
from django.apps import apps
from django.contrib.auth.models import Group
from .models import Comment, Post, Category

admin.site.unregister(Group)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


models = apps.get_models()
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        # admin.site.unregister(model)
        pass

