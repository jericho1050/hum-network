import json
from json import JSONDecodeError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt


from .models import User, Post, Likes, Follow
from .forms import UserProfilePicForm, PostModelForm

def index(request):
    form = PostModelForm()
    posts = Post.objects.all().order_by('-post_time')

    # checks if user has like a particular post
    for post in posts:
        post.user_has_liked = request.user in post.liked_by_users()
            
    paginator = Paginator(posts, 10)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "form": form,
        "posts": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    

@login_required
def post(request):
    
    # creating a post must be via POST or PUT
    if request.method != "POST" and request.method != "PUT":
        return JsonResponse({"error": "POST or PUT request required."}, status=400)
    
    data = json.loads(request.body)

    # edit content
    if request.method == "PUT":
        print(data)
        content = data.get("content")
        post = Post.objects.get(id=data["post_id"])
        post.content = content
        post.save()


    else:
        # check post's content
        content = data.get("content")

        post = Post()
        post.content = content
        post.post_by = request.user
        post.save()

    return JsonResponse({"edited_conntent": content}, status=201)


# profile page of the user
def profile(request, profile_id):
    # Query for requested user's profile
    try:
        profile = User.objects.get(pk=profile_id)
        posts = profile.posts.all().order_by('-post_time')
    except User.DoesNotExist:
        return JsonResponse({"error": "Profile not found."}, status=404)
    
    # checks if user has like a particular post
    for post in posts:
        post.user_has_liked = request.user in post.liked_by_users()
    
    # pagination implementation
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # uploads a profile picture
    if request.method == "POST":
        form = UserProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data
            profile.profile_picture = img['profile_picture']
            profile.save()

    if request.user.is_authenticated:
        is_followed = Follow.objects.filter(followee=profile, follower=request.user).exists()
    else:
        is_followed = False
            

    return render(request, "network/profile.html", {
        "profile": profile,
        "form": UserProfilePicForm(),
        "posts":page_obj,
        "is_followed": is_followed,
    })

def follow(request):
    # POST request required
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    try:
        data = json.loads(request.body)
        print(data)
    except JSONDecodeError:
        return JsonResponse({"error": "Invalid or no JSON received"}, status=400)
    
    
    if data.get("follower") is not None and data.get("followee") is not None:
        # query for these users for validation
        try:
            follower = User.objects.get(username=data.get("follower"))
            followee = User.objects.get(username=data.get("followee"))
        except User.DoesNotExist:
            return JsonResponse({"error": "Users not found"}, status=404)
        
        # follows user
        if data.get("action") == 'follow':
            Follow.objects.create(follower=follower, followee=followee)
        
        # unfollows user
        else:
            try:
                unfollow = Follow.objects.get(follower=follower, followee=followee)
            except Follow.DoesNotExist:
                return JsonResponse({"error": "Follow Assertion not found"}, status=404)
            unfollow.delete()

    return JsonResponse({"message": "user followed or unfollowed"}, status=201)

@login_required
def following(request):
    # All posts by followed users
    following = Follow.objects.filter(follower=request.user).values_list("followee", flat=True)
    posts = Post.objects.filter(post_by__in=following).order_by('-post_time')

        # checks if user has like a particular post
    for post in posts:
        post.user_has_liked = request.user in post.liked_by_users()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": page_obj
    })

@csrf_exempt
@login_required
def like(request, post_id):
    
    # like  POST request
    if request.method == "POST":
        data = json.loads(request.body)
        if all(data.get(key) is not None for key in ['post_id', 'action']):

            # query for post liked
            try:
                post = Post.objects.get(id=data["post_id"])
            except Post.DoesNotExist:
                return JsonResponse({"message": "Post not found"}, status=404)
            
            # if like action create object
            if data.get("action") == "like":
                like = Likes()
                like.liked_by = request.user
                like.post_liked = post
                post.like_count += 1
                post.save()
                like.save()
                
            # if unlike action delete like object
            else:
                try:
                    post.like_count -= 1
                    post.save()
                    unlike = Likes.objects.filter(liked_by = request.user, post_liked = post)
                    unlike.delete()
                    
                    return JsonResponse({"message": "post unliked!"}, status=201)

                except Likes.DoesNotExist:
                    return JsonResponse({"message": "Likes Ojbect not found"}, status=404)
                
        return JsonResponse({"message": "post liked!"}, status=200)  

    if request.method == "GET":
        return JsonResponse({"message": "No GET here"}, status=400)
            



        

