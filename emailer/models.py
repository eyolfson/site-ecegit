from django.contrib.auth.models import User
from django.db import models

from django_gitolite.models import Repo

class Notification(models.Model):
    user = models.ForeignKey(User, related_name="notifications")
    repo = models.ForeignKey(Repo, related_name="notifications")

    class Meta:
        unique_together = ("user", "repo")
