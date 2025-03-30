from django.contrib import admin

from .models import User, Post, Likes, Follow, Comment, ChatMessage

# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Likes)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(ChatMessage)
