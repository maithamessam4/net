from django.urls import path

from . import views

urlpatterns = [

    path('like_update/<int:post_id>' , views.like_update,name = 'like_update'),
    path('edit_post/<int:post_id>' , views.edit_post ,name ='edit_post'),
    path('following' , views.following , name = 'following'),
    path('unfollow_user/<int:from_user>' , views.unfollow_user , name= 'unfollow_user'),
    path('follow_user/<int:to_user>' , views.follow_user , name='follow_user'),
    path('profile/<int:id>' , views.profile, name = 'profile'),
    path('newpost' , views.new_post , name='newpost'),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]