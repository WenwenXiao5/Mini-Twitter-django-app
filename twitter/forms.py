from django.forms import ModelForm
from .models import Tweet, Comment

class TweetForm(ModelForm):
    class Meta:
        model = Tweet
        fields = [
            'content'
        ]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]