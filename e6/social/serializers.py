from .models import *
from rest_framework import serializers

class MessageSerializer( serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'sender', 'time', 'room']
        read_only_fields = ('sender', 'room')
    def create(self, validated_data):
        usersender = self.context['request'].user
        usernamerec = self.context['request'].data['usernamerec']
        if usernamerec:
            userrec = User.objects.get(username=usernamerec)
            room = Room.objects.filter(ischat=True, members=usersender).filter(members=userrec).first()

        msg = Message.objects.create(
            text = validated_data['text'],
            sender = self.context['request'].user,
            room=room,
        )
        return msg

class UserSearchByUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ]

