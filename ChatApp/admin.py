from django.contrib import admin


from .models import *

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(ChatRoom)
admin.site.register(singleMessage)