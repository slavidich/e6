from django.contrib import admin
from django.contrib.auth.admin import admin

from .models import Profile, ChatMessages, Message, Room
# Register your models here.

class ChatMembers(admin.TabularInline):
    model = ChatMessages
    extra = 2

class ChatAdmin (admin.ModelAdmin):
    inlines = (ChatMembers,)

admin.site.register(Profile)
admin.site.register(ChatMessages)
admin.site.register(Message)
admin.site.register(Room, ChatAdmin)
