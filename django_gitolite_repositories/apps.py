# Copyright 2015 Jon Eyolfson
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class GitoliteRepositoriesConfig(AppConfig):
    name = 'django_gitolite_repositories'

    def ready(self):
        if settings.DEBUG:
            from django_gitolite_repositories.version import get_version
            print('django-gitolite-repositories {}'.format(get_version()))
