from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='images/', height_field=None, width_field=None, null=True, blank=True, verbose_name="")

class Post(models.Model):
    content = models.TextField(verbose_name="", blank=False)
    post_date = models.DateField(auto_now_add=True)
    post_time = models.DateTimeField(auto_now_add=True)
    post_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.post_by}: {self.content}"
    
    def liked_by_users(self):
        return [like.liked_by for like in self.likes_set.all()]

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
    comment_to = models.ForeignKey(Post, on_delete=models.CASCADE)
