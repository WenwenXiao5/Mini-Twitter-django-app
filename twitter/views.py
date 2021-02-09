from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.conf import settings


from django.shortcuts import render, get_object_or_404, redirect

from .forms import CommentForm, TweetForm
from .models import Tweet, Follow

@login_required()
def index(request):
    followings = request.user.following.all()
    tweets = []
    for following in followings:
        user = following.user_to
        user_tweets = Tweet.objects.filter(user=user)[:5]
        for t in user_tweets:
            tweets.append(t)
    context = {
        'user': request.user,
        'tweets': tweets
    }
    # current_user = request.user
    # return render(request, 'twitter/index.html', {'username' : current_user.username})
    return render(request, 'twitter/index.html', context)


def signup(request):
    if request.method == 'POST':
        form =UserCreationForm(request.POST)
        if form.is_valid():
            # Save user
            form.save()
            # log user in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            # login page
            login(request, user)
            # redirect
            return redirect('twitter:index')
        # There is no else atatement. If the form is not valid 
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form' : form})

def logout_user(request):
    logout(request)
    return redirect('twitter:index')

# page to create a new tweet as a logged-in userz
@login_required()   
def compose_tweet(request):
    current_user = request.user
    if request.method == 'POST':
        form =TweetForm(request.POST)
        if form.is_valid():
            # Save tweet content, but do not commit
            new_tweet = form.save(commit=False)
            # log user in
            new_tweet.user_id = current_user.id
            new_tweet.save()
            # redirect
            return redirect('twitter:index')
        # There is no else atatement. If the form is not valid 
    else:
        form = TweetForm()
    return render(request, 'twitter/compose_tweet.html', {'form' : form})

# The above compose_tweet method can also be written as below 
# @login_required()
# # page to create a new tweet as logged in user
# def compose_tweet(request):
#   current_user = request.user
#   user = User.objects.get(id=current_user.id)
#   if request.method == 'POST':
#     form = TweetForm(request.POST)
#     if form.is_valid():
#       new_tweet = form.save(commit=False) # use commit=False to delay write (cuz we need to update the user field)
#       new_tweet.user = user
#       new_tweet.save()
#       return redirect('twitter:user', current_user.id)
#   else:
#     form = TweetForm()
#   context = {
#     'form': form
#   }
#   return render(request, 'twitter/compose_tweet.html', context)


# Tweet page, shows the tweet and all its comments      ``
def tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    comments = tweet.comments
    # create a context dictionary 
    context = {
        'tweet' : tweet,
        'comments' : comments,
        'current_user' : request.user,  
    }
    # If it's a POST request, then validate the form and create new_comment
    # If it's a GET request, then show the tweet, all its comments and the form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.tweet = tweet
            new_comment.user = request.user
            new_comment.save()
    else:
        form = CommentForm()
    context['comment_form'] = form
    return render(request, 'twitter/tweet.html', context)


# User page, shows user name, following and follower, follow/unfollow toggle, and the first 20 tweets
@login_required
def user(request, user_id):
    current_user = request.user
    user = get_object_or_404(User, pk=user_id)
    tweets = user.tweets.all()[:20]
    context = {
        'current_user': current_user,
        'user': user,
        'tweets': tweets,
    }

# Check if the current user is already following the page's user
    already_following = Follow.objects.filter(user_from=current_user, user_to=user_id).exists()
    context['is_following'] = already_following
    if request.method == 'POST':
        if already_following:
            # To unfollow
            follow = Follow.objects.get(user_from=current_user, user_to=user_id)
            follow.delete()
        else:
        # To follow
            follow = Follow(user_from=current_user, user_to=user)
            follow.save()
        return redirect('twitter:user', user_id)
    return render(request, 'twitter/user.html', context)


