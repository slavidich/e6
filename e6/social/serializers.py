from .models import *
from rest_framework import serializers

class MessageSerializer( serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'time']