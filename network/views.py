import json
from json import JSONDecodeError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt


from .models import User, Post, Likes, Follow, Comment
from .forms import UserProfilePicForm, PostModelForm, PostForm

@login_required
def index(request):
    if request.method == "POST":
        # This handles the HTMX post creation submission
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            # Check if it's an HTMX request
            if request.htmx:
                # Render only the new post partial and return it
                html = render_to_string('network/_post.html', {'post': post}, request=request)
                # Prepend the new post to the feed using hx-swap="afterbegin" on the form
                return HttpResponse(html)
            else:
                # For non-HTMX POST, redirect back to index (standard form submission)
                return redirect('index')
        else:
            # Handle invalid form submission, potentially returning errors
            if request.htmx:
                return HttpResponseBadRequest("Invalid post content.") # Simplistic error handling
            else:
                # Re-render the page with the form containing errors (standard approach)
                posts = Post.objects.all().order_by('-timestamp') # Or your specific query
                return render(request, 'network/index.html', {'form': form, 'posts': posts})

    # GET Request: Display the feed and the empty post form
    form = PostForm()
    posts = Post.objects.all().order_by('-timestamp') # Adjust query as needed (e.g., following)
    
    # Add user_has_liked attribute to each post
    for post in posts:
        if request.user.is_authenticated:
            post.user_has_liked = Likes.objects.filter(liked_by=request.user, post_liked=post).exists()
        else:
            post.user_has_liked = False
    
    # Paginate the posts
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    # Create common context
    context = {
        'form': form, 
        'posts': page_obj,
        'current_page': 'all_posts',
        'current_filter': 'all_posts'
    }
    
    # If it's an HTMX request, handle differently based on the request parameters
    if request.htmx:
        # Check if we're just filtering posts or doing a full page navigation
        if request.GET.get('filter') == 'true':
            # Only return the post feed area for filter buttons
            return render(request, 'network/_post_feed_area.html', context)
        else:
            # This is a full navigation request from nav bar
            return render(request, 'network/index_content.html', context)
    
    # For regular page load, render the full page with context
    return render(request, 'network/index.html', context)


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
            context = {
                "message": "Invalid username and/or password."
            }
            
            # For HTMX requests, return content-only template
            if request.htmx:
                return render(request, "network/login_content.html", context)
            else:
                return render(request, "network/login.html", context)
    else:
        # For HTMX requests, return content-only template
        if request.htmx:
            return render(request, "network/login_content.html")
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
            context = {
                "message": "Passwords must match."
            }
            
            # For HTMX requests, return content-only template
            if request.htmx:
                return render(request, "network/register_content.html", context)
            else:
                return render(request, "network/register.html", context)

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            context = {
                "message": "Username already taken."
            }
            
            # For HTMX requests, return content-only template
            if request.htmx:
                return render(request, "network/register_content.html", context)
            else:
                return render(request, "network/register.html", context)
                
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        # For HTMX requests, return content-only template
        if request.htmx:
            return render(request, "network/register_content.html")
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
        post.author = request.user
        post.save()

    return JsonResponse({"edited_conntent": content}, status=201)


# profile page of the user
def profile(request, profile_id):
    # Query for requested user's profile
    try:
        profile = User.objects.get(pk=profile_id)
        posts = profile.posts.all().order_by('-timestamp')
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
    
    context = {
        "profile": profile,
        "form": UserProfilePicForm(),
        "posts": page_obj,
        "is_followed": is_followed,
        "current_page": "profile"
    }
    return render(request, "network/profile.html", context)

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
    posts = Post.objects.filter(author__in=following).order_by('-timestamp')

    # checks if user has like a particular post
    for post in posts:
        post.user_has_liked = request.user in post.liked_by_users()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Create common context
    context = {
        'posts': page_obj,
        'current_page': 'following'
    }

    # If it's an HTMX request, handle differently based on the request parameters
    if request.htmx:
        # Check if we're just filtering posts or doing a full page navigation
        if request.GET.get('filter') == 'true':
            # Only return the post feed area for filter buttons
            return render(request, 'network/_post_feed_area.html', context)
        else:
            # This is a full navigation request from nav bar
            return render(request, 'network/following_content.html', context)

    # For regular page load, render the full page
    return render(request, "network/following.html", context)

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
            

@login_required
def toggle_like(request, post_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Method not allowed")

    post = get_object_or_404(Post, id=post_id)
    
    # Check if the user has already liked this post
    like_exists = Likes.objects.filter(liked_by=request.user, post_liked=post).exists()
    
    if like_exists:
        # Unlike the post
        post.like_count -= 1
        post.save()
        Likes.objects.filter(liked_by=request.user, post_liked=post).delete()
        liked = False
    else:
        # Like the post
        post.like_count += 1
        post.save()
        like = Likes(liked_by=request.user, post_liked=post)
        like.save()
        liked = True
    
    # For HTMX requests, return the updated like button partial
    if request.headers.get('HX-Request') == 'true':
        context = {
            'post': post, 
            'liked': liked, 
            'like_count': post.like_count
        }
        html = render_to_string('network/_like_button.html', context, request=request)
        return HttpResponse(html)
    else:
        # Fallback for non-HTMX requests
        return redirect(request.META.get('HTTP_REFERER', 'index'))

# Add functions for post editing and deletion
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author
    if request.user != post.author:
        return HttpResponseBadRequest("You cannot edit this post")
    
    if request.method == "GET":
        # Return the edit form
        context = {'post': post}
        html = render_to_string('network/_edit_post_form.html', context, request=request)
        return HttpResponse(html)
    
    elif request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            # Return the updated post content
            context = {'post': post}
            html = render_to_string('network/_post_content.html', context, request=request)
            return HttpResponse(html)
        else:
            # Return form with errors
            context = {'post': post, 'form': form}
            html = render_to_string('network/_edit_post_form.html', context, request=request)
            return HttpResponse(html)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author
    if request.user != post.author:
        return HttpResponseBadRequest("You cannot delete this post")
    
    if request.method == "DELETE":
        post.delete()
        return HttpResponse("")  # Empty response as the post is removed from DOM
    
    return HttpResponseBadRequest("Method not allowed")

@login_required
def cancel_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Return the post content without edit form
    context = {'post': post}
    html = render_to_string('network/_post_content.html', context, request=request)
    return HttpResponse(html)

def load_more(request):
    """Load more posts for infinite scroll"""
    page_number = request.GET.get('page', 1)
    posts = Post.objects.all().order_by('-timestamp')
    
    # Determine if we're filtering by following
    is_following_feed = request.GET.get('following') == 'true'
    
    # Check if we're filtering by following
    if is_following_feed and request.user.is_authenticated:
        following = Follow.objects.filter(follower=request.user).values_list("followee", flat=True)
        posts = posts.filter(author__in=following)
    
    # Add user_has_liked attribute for rendering likes correctly
    for post in posts:
        if request.user.is_authenticated:
            post.user_has_liked = Likes.objects.filter(liked_by=request.user, post_liked=post).exists()
        else:
            post.user_has_liked = False
    
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_obj = paginator.get_page(page_number)
    
    # Note: The first load of following/all posts is now handled by the following/index views
    # directly, so this is only for infinite scroll of additional pages
    
    # Render just the additional posts list for the infinite scroll
    context = {
        'posts': page_obj
    }
    html = render_to_string('network/_posts_list.html', context, request=request)
    return HttpResponse(html)

@login_required
def toggle_follow(request, profile_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Method not allowed")
    
    # Get the profile to follow/unfollow
    profile = get_object_or_404(User, id=profile_id)
    
    # Don't allow following yourself
    if request.user == profile:
        return HttpResponseBadRequest("You cannot follow yourself")
    
    # Check if already following
    follow_exists = Follow.objects.filter(follower=request.user, followee=profile).exists()
    
    if follow_exists:
        # Unfollow
        Follow.objects.filter(follower=request.user, followee=profile).delete()
        is_followed = False
    else:
        # Follow
        follow = Follow(follower=request.user, followee=profile)
        follow.save()
        is_followed = True
    
    # For HTMX requests, return the updated follow button
    if request.headers.get('HX-Request') == 'true':
        context = {'profile': profile, 'is_followed': is_followed, 'user': request.user}
        html = render_to_string('network/_follow_button.html', context, request=request)
        return HttpResponse(html)
    else:
        # Fallback for non-HTMX requests
        return redirect('profile', profile_id=profile_id)

@login_required
def get_comments(request, post_id):
    """Get comments for a specific post."""
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(comment_to=post).order_by('id')
    
    context = {
        'post': post,
        'comments': comments,
        'user': request.user
    }
    
    html = render_to_string('network/_comments.html', context, request=request)
    return HttpResponse(html)

@login_required
def add_comment(request, post_id):
    """Add a comment to a post."""
    if request.method != "POST":
        return HttpResponseBadRequest("Method not allowed")
    
    post = get_object_or_404(Post, id=post_id)
    comment_text = request.POST.get('comment', '').strip()
    
    if not comment_text:
        return HttpResponseBadRequest("Comment cannot be empty")
    
    # Create the comment
    comment = Comment(
        comment=comment_text,
        comment_by=request.user,
        comment_to=post,
        timestamp=timezone.now()
    )
    comment.save()
    
    # Get all comments for this post to return the updated list
    comments = Comment.objects.filter(comment_to=post).order_by('id')
    
    context = {
        'post': post,
        'comments': comments,
        'user': request.user
    }
    
    html = render_to_string('network/_comments.html', context, request=request)
    return HttpResponse(html)

@login_required
def delete_comment(request, comment_id):
    """Delete a comment."""
    if request.method != "DELETE":
        return HttpResponseBadRequest("Method not allowed")
    
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Check if user is authorized to delete this comment
    if request.user != comment.comment_by:
        return HttpResponseBadRequest("You cannot delete this comment")
    
    comment.delete()
    
    # Return an empty response as the comment div will be removed
    return HttpResponse("")




        

