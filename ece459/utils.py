import logging
import os
import subprocess

from django_gitolite.utils import home_dir

logger = logging.getLogger('ece459')

def is_ece459_key(key):
    command = ['gitolite', 'list-memberships', '-u', key.user.username]
    o = subprocess.check_output(command, stderr=subprocess.DEVNULL)
    for l in o.splitlines():
        if l == b'@ece459-1141-students':
            return True
    return False

def key_abspath(key):
    filename = '{}@django-{}.pub'.format(key.user.username, key.pk)
    return os.path.join(home_dir(), 'ece459-1-keydir', filename)

def receive_key_create(sender, instance, **kwargs):
    if not is_ece459_key(instance):
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
    if not is_ece459_key(instance):
        return
    path = key_abspath(instance)
    try:
        os.remove(path)
    except:
        msg = "key with path '{}' not deleted"
        logger.error(msg.format(path))
