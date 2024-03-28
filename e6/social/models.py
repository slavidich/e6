from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.shortcuts import redirect
from django.urls import reverse


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
    def __str__(self):
        return f'Профиль {self.user.username}'

class Room(models.Model):
    ischat = models.BooleanField(default=True, blank=False)
    members = models.ManyToManyField(User, through='ChatMessages', related_name='members')
    roomname = models.SlugField(max_length=50, null=True)
    admin = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        if self.ischat:
            return f'Чат между {self.members.all()}'
        else:
            return f'Групповой чат {self.roomname}'
    def get_absolute_url(self):
        return reverse('room', kwargs={'roomname':self.roomname})

class Message(models.Model):
    text = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('time',)

class ChatMessages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)