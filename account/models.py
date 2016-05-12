from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
from django.conf import settings

"""
    Datebase object for Invite Keys
"""
@python_2_unicode_compatible
class InviteKey(models.Model):
    invite_key = models.CharField(max_length=1000)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return self.invite_key
