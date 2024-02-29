from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 300,300
        if self.avatar:
            image = Image.open(self.avatar.path)
            image.thumbnail(SIZE, Image.LANCZOS)
            image.save(self.avatar.path)