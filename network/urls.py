from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),

    # HTMX Routes
    path("toggle_like/<int:post_id>/", views.toggle_like, name="toggle_like"),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("cancel_edit/<int:post_id>/", views.cancel_edit, name="cancel_edit"),
    path("load_more/", views.load_more, name="load_more"),
    path("toggle_follow/<int:profile_id>/", views.toggle_follow, name="toggle_follow"),
    path("get_comments/<int:post_id>/", views.get_comments, name="get_comments"),
    path("add_comment/<int:post_id>/", views.add_comment, name="add_comment"),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),

    # API Routes
    path("posts", views.post, name="post"),
    path("follow", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
]
