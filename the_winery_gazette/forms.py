from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """ Form to allow commenting on gazette posts """

    class Meta:
        model = Comment
        fields = ('author', 'body')
