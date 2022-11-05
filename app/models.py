from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from taggit.managers import TaggableManager

from helpers.models import BaseModel
from common.models import User


class Category(BaseModel):
    title = models.CharField(max_length=64, null=True)
    slug = models.SlugField(blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    post_count = models.PositiveIntegerField(default=0)

    def postCount(self):
        count = Post.objects.all().filter(category=self.category).count()
        self.post_count = count
        return self.post_count

    def save(self, *args, **kwargs):
        self.post_count = Post.objects.all().filter(category=self.id).count()
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Post(BaseModel):
    title = models.CharField(max_length=256)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()

    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')
    tag = TaggableManager()

    comments_count = models.IntegerField(verbose_name="Total Comments", default=0)

    def comment_count(self):
        count = Comment.objects.all().filter(post=self.id).count()
        return count

    def user_post_count(self):
        print(dir(self))
        count = Post.objects.all().filter(author__username=self).count()
        return count

    def save(self, *args, **kwargs):
        self.comments_count = Comment.objects.all().filter(post=self.id).count()
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk, 'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)

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
