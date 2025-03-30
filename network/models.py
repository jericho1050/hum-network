from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='images/', height_field=None, width_field=None, null=True, blank=True, verbose_name="")

class Post(models.Model):
    content = models.TextField(verbose_name="", blank=False)
    post_date = models.DateField(auto_now_add=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author}: {self.content}"
    
    def liked_by_users(self):
        return [like.liked_by for like in self.likes_set.all()]
    
    @property
    def post_time(self):
        return self.timestamp
    
    @property
    def post_by(self):
        return self.author
        
    @property
    def comment_count(self):
        return self.comments.count()

class Likes(models.Model):
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post_liked = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.liked_by} likes {self.post_liked}"

class Follow(models.Model):
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', null=True)

    def __str__(self):
        return f"Follower:{self.follower} Following: {self.followee}"
    

class Comment(models.Model):
    comment = models.TextField()
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_to = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.comment_by} commented on {self.comment_to}"

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['sender', 'receiver', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content[:50]}"
