from django.contrib import admin

# Register your models here.
from . models import Room, Message, Topic     #.models is done as it is in same room

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)


