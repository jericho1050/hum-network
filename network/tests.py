from django.test import TestCase, Client

from .models import User, Post, Likes, Follow


# Create your tests here.


class NetworkTestcase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.user.set_password('testpassword')
        self.user.save()
        self.user2 = User.objects.create(username='testuser2')
        self.user3 = User.objects.create(username="testuser3")

        Post.objects.create(content="TEST", post_by=self.user)
        Post.objects.create(content="test", post_by=self.user2)

    def test_post_creation(self):
        post = Post.objects.create(content='Test content', post_by=self.user)

        self.assertEqual(post.content, 'Test content')
        self.assertEqual(post.post_by, self.user)
        self.assertEqual(post.like_count, 0)

    def test_post_like(self):
        post = Post.objects.create(content='Test', post_by=self.user, like_count=69)

        self.assertEqual(post.like_count, 69)

    def test_likes_post(self):
        post = Post.objects.create(content='Test Liking', post_by=self.user, like_count=1)
        like = Likes.objects.create(liked_by=self.user2, post_liked=post)

        self.assertEqual(like.liked_by, self.user2)
        self.assertEqual(post.post_by, self.user)
        self.assertEqual(like.post_liked, post)

    def test_follow(self):
        follow = Follow.objects.create(follower=self.user2, followee=self.user)

        self.assertEqual(follow.follower, self.user2)
        self.assertEqual(follow.followee, self.user)

    def test_followers(self):
        Follow.objects.create(follower=self.user2, followee=self.user)
        Follow.objects.create(follower=self.user3, followee=self.user)

        self.assertEqual(self.user.followers.count(), 2)


    def test_like_unlike(self):
        post = Post.objects.create(content='Test', post_by=self.user)
        like = Likes.objects.create(liked_by=self.user2, post_liked=post)
        post.like_count = 1
        self.assertEqual(post.like_count, 1)

        post.like_count -= 1

        self.assertEqual(post.like_count, 0)

    def test_follow_unfollow(self):
        follow = Follow.objects.create(follower=self.user2, followee=self.user)
        self.assertEqual(self.user.followers.count(), 1)
        self.assertEqual(self.user2.following.count(), 1)

        follow.delete()

        self.assertEqual(self.user.followers.count(), 0)
        self.assertEqual(self.user2.following.count(), 0)

    def test_index(self):
        c = Client()
        response = c.get("/")        
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["posts"]), 2)

    def test_profile(self):
        c = Client()

        response = c.get(f"/profile/{self.user.id}")
        response2 = c.get(f"/profile/{self.user2.id}")
        response3 = c.get(f"/profile/{self.user3.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

        self.assertEqual(len(response.context["posts"]), 1)

    def test_following(self):
        c = Client()
        c.login(username=self.user.username, password='testpassword')

        Follow.objects.create(follower=self.user, followee=self.user2)
        Follow.objects.create(follower=self.user, followee=self.user3)

        Post.objects.create(content="TEST", post_by=self.user)
        Post.objects.create(content="TEST", post_by=self.user3)
        Post.objects.create(content="TEST", post_by=self.user3)

        response = c.get("/following")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 3)


