import logging
import os
import subprocess

from django.contrib.auth.models import User

from django_gitolite.utils import home_dir
from django_ssh.models import Key

GITOLITE_STUDENT_GROUP = '@ece459-1161-students'

logger = logging.getLogger('ece459_1161')

def is_student(username):
    command = ['gitolite', 'list-memberships', '-u', username]
    o = subprocess.check_output(command, stderr=subprocess.DEVNULL,
                                universal_newlines=True)
    for l in o.splitlines():
        if l == GITOLITE_STUDENT_GROUP:
            return True
    return False

def is_student_key(key):
    return is_student(key.user.username)

def key_abspath(key):
    filename = '{}@django-{}.pub'.format(key.user.username, key.pk)
    return os.path.join(home_dir(), 'ece459-1-keydir', filename)

def receive_key_create(sender, instance, **kwargs):
    if not is_student_key(instance):
        return
    path = key_abspath(instance)
    try:
        with open(path, 'w') as f:
            f.write(instance.data)
            f.write('\n')
    except:
        msg = "key with path '{}' not created"
        logger.error(msg.format(path))

def receive_key_delete(sender, instance, **kwawgs):
    if not is_student_key(instance):
        return
    path = key_abspath(instance)
    try:
        os.remove(path)
    except:
        msg = "key with path '{}' not deleted"
        logger.error(msg.format(path))

def sync():
    command = ['gitolite', 'list-members', GITOLITE_STUDENT_GROUP]
    o = subprocess.check_output(command, stderr=subprocess.DEVNULL,
                                universal_newlines=True)
    for l in o.splitlines():
        try:
            user = User.objects.get(username=l)
            for key in user.ssh_keys.all():
                receive_key_create(Key, key)
        except User.DoesNotExist:
            pass
