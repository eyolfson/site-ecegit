import logging
import os
import subprocess

from django.contrib.auth.models import User

from django_gitolite.utils import key_abspath
from django_ssh.models import Key

GITOLITE_STUDENT_GROUP = '@ece459-1161-students'

logger = logging.getLogger('ece459_1161')

def is_student(username):
    command = ['gitolite', 'list-memberships', '-u', username]
    try:
        o = subprocess.check_output(command, stderr=subprocess.DEVNULL,
                                    universal_newlines=True)
    except Exception as e:
        logger.error("gitolite command failed")
        return False
    for l in o.splitlines():
        if l == GITOLITE_STUDENT_GROUP:
            return True
    return False

def is_student_key(key):
    return is_student(key.user.username)

def receive_key_create(sender, instance, **kwargs):
    if not is_student_key(instance):
        return
    path = key_abspath(instance)
    try:
        subprocess.check_call(['scp', path,
            'ecegitcontroller@ece459-1.uwaterloo.ca:keydir-1161/'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        msg = "key with path '{}' not scp'ed"
        logger.error(msg.format(path))

def receive_key_delete(sender, instance, **kwawgs):
    if not is_student_key(instance):
        return
    path = key_abspath(instance)
    try:
        keybase = os.path.basename(path)
        subprocess.check_call(['ssh', 'rm',
            'ecegitcontroller@ece459-1.uwaterloo.ca:keydir-1161/{}'.format(keybase)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
