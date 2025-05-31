from django.contrib import admin
from .models import User, Conversation, Messages

admin.site.register(User)
admin.site.register(Conversation)
admin.site.register(Messages)
