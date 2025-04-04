from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("users/", views.user_list_view, name="user_list"),  # New URL for user list page

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
    path("edit_comment/<int:comment_id>/", views.edit_comment, name="edit_comment"),
    path("update_comment/<int:comment_id>/", views.update_comment, name="update_comment"),
    path("cancel_edit_comment/<int:comment_id>/", views.cancel_edit_comment, name="cancel_edit_comment"),

    # Chat Routes
    path("messages/", views.conversation_list_view, name="conversation_list"),
    path("chat/<str:username>/", views.chat_view, name="chat"),
    path("chat/<str:username>/send/", views.send_message_view, name="send_message"),
    path("chat/<str:username>/poll/", views.poll_new_messages_view, name="poll_messages"),

    # API Routes
    path("posts", views.post, name="post"),
    path("follow", views.follow, name="follow"),
    path("like/<int:post_id>", views.like, name="like"),
]
