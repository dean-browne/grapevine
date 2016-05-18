from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from django import forms
from .models import Post, Comment


"""
Form for: Adding a Post
"""
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('post',)
        widgets = {
            'post': SummernoteWidget(attrs={'height': '400px'}),
        }


"""
Form for: adding a Comment
"""
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)
        wigets = {
            'comment': forms.Textarea(attrs={'class': 'comment-form-textarea'}),
        }
