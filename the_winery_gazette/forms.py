from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    """ Form to allow commenting on gazette posts """

    class Meta:
        model = Comment
        fields = ('author', 'body')


class PostArticleForm(forms.ModelForm):
    """ Form to add posts """

    class Meta:
        model = Post
        fields = ('title', 'slug', 'image', 'content', 'status')
