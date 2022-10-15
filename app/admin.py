from django.contrib import admin
from django.apps import apps
from django.contrib.auth.models import Group
from .models import Comment, Post, Category
from taggit.models import Tag

admin.site.unregister(Group)
admin.site.register(Category)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tag_list')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tag')

    def tag_list(self, obj):
        return u", ".join([tag.name for tag in obj.tag.all()])


# models = apps.get_models()
# for model in models:
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         # admin.site.unregister(model)
#         pass

