from django.db import models
from django.urls import reverse
from helpers.models import BaseModel
from common.models import User

# Create your models here.

# instead of using auto_now_add or auto_now use below
# from django.utils import timezone
# date_posted = models.DateTimeField(default=timezone.now)

class Category(BaseModel):
    title = models.CharField(max_length=64, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

class Post(BaseModel):
    title = models.CharField(max_length=256)
    content = models.TextField()

    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Comment(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content = models.TextField(verbose_name='Text comment')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return self.user.username

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})
