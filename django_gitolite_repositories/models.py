# Copyright 2015 Jon Eyolfson
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

from django.db import models

from django_gitolite.models import Repo

class Lock(models.Model):
    repo = models.OneToOneField(Repo, primary_key=True)

    def __str__(self):
        return str(self.repo)
