# Copyright 2015 Jon Eyolfson
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

from django.conf import settings

from django_gitolite_repositories.models import Lock

from django_gitolite.utils import home_dir, gitolite_command_prefix

import logging
import os

logger = logging.getLogger('gitolite_repositories')

class LockedRepo:

    def __init__(self, repo):
        self.repo = repo
        self.lock = None

    def __enter__(self):
        self.lock, created = Lock.objects.get_or_create(repo=self.repo)
        retries = 0
        max_retries = 50
        while not created:
            if retries >= max_retries:
                logger.error("'{}' could not acquire lock".format(name))
                raise Exception('Lock error, check logs')
            sleep(0.1)
            self.lock, created = Lock.objects.get_or_create(repo=self.repo)
            retries += 1

        # git itself or gitolite defines this as part of the hook, which
        # causes any following git commands to fail after changing to the
        # work directory
        if 'GIT_DIR' in os.environ:
            del environ['GIT_DIR']

        repository_path = path.join(settings.BASE_DIR, 'repositories',
                                    self.repo.path)
        if not path.isdir(repository_path):
            base_dir, repository_dir = path.split(repository_path)
            if not path.isdir(base_dir):
                makedirs(base_dir)
            chdir(base_dir)
            git_dir_path = path.join(home_dir(), 'repositories',
                                     '{}.git'.format(name))
            git_call(['clone', git_dir_path])
            chdir(repository_dir)
        else:
            chdir(repository_path)
            git_call(['pull', 'origin', 'master'])

        if 'master' in git_call(['branch']):
            git_call(['reset', '--hard', 'master'])
        else:
            logger.warning("Empty repository '{}'".format(name))
        return self.lock

    def __exit__(self, type, value, traceback):
        # Release the lock
        if self.lock:
            self.lock.delete()
        pass
