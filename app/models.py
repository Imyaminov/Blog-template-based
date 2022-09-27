from django.db import models
from django.urls import reverse
from helpers.models import BaseModel
from common.models import User

# Create your models here.

# instead of using auto_now_add or auto_now use below
# from django.utils import timezone
# date_posted = models.DateTimeField(default=timezone.now)

class Post(BaseModel):
    title = models.CharField(max_length=256)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
