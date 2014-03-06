from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete

from django_gitolite.models import Repo
from django_ssh.models import Key

from ece459.utils import receive_key_create, receive_key_delete

class Assignment(models.Model):
    slug = models.SlugField()

class Group(models.Model):
    assignment = models.ForeignKey(Assignment, related_name='groups')
    members = models.ManyToManyField(User, related_name='ece459_groups')
    repo = models.ForeignKey(Repo, blank=True, null=True)

class TestbotMessage(models.Model):
    group = models.ForeignKey(Group, related_name='testbot_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-timestamp']

class TSPResult(models.Model):
    group = models.OneToOneField(Group, related_name='tsp_result')
    iterations = models.IntegerField()
    distance = models.FloatField()

    class Meta:
        ordering = ['-iterations', 'distance']

# Signals
post_save.connect(receive_key_create, Key)
pre_delete.connect(receive_key_delete, Key)
