from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
from django.conf import settings


"""
Database object for: Post
"""
@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=400)
    post = models.TextField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.post

"""
Database object for: Comment
"""
@python_2_unicode_compatible
class Comment(models.Model):
    comment = models.TextField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # Add points here!
    votes = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.comment
