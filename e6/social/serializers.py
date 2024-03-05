from .models import *
from rest_framework import serializers

class MessageSerializer( serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'time', 'room']
        read_only_fields = ('sender', 'room')
    def create(self, validated_data):
        msg = Message.objects.create(
            text = validated_data['text'],
            sender = User.objects.get(username='admin'),#self.context['request'].user,
            room=Room.objects.get(id=1),
        )
        return msg

