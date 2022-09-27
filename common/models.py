from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from PIL import Image
# Create your models here.

class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={
            "error": 'This email already exists!',
        },
    )
    username = models.CharField(
        max_length=128,
        unique=True,
        error_messages={
            "error": 'This username already exists!',
        },
    )
    # firstname = models.CharField(max_length=128, null=True)
    # lastname = models.CharField(max_length=128, null=True)
    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(8)],
        error_messages={
            'error': 'Password must contain at least 8 characters'
        }
    )

    bio = models.CharField(max_length=128, blank=True)
    avatar = models.ImageField(default='default.jpg', upload_to='profile/')

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            size = (300, 300)
            img.thumbnail(size)
            img.save(self.avatar.path)

