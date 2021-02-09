from django.urls import path

from . import views

app_name = 'twitter'
urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout_user, name='logout'),
    path('tweets/<int:tweet_id>', views.tweet, name='tweet'),
    path('users/<int:user_id>', views.user, name='user'),
    path('compose_tweet', views.compose_tweet, name='compose_tweet')
]