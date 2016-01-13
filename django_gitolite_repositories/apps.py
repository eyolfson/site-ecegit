# Copyright 2015-2016 Jonathan Eyolfson
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

from django.apps import AppConfig
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

class GitoliteRepositoriesConfig(AppConfig):
    name = 'django_gitolite_repositories'

    def ready(self):
        if settings.DEBUG:
            from django_gitolite_repositories.version import get_version
            print('django-gitolite-repositories {}'.format(get_version()))
