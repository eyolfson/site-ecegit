import logging
import os
import subprocess

from django_gitolite.utils import home_dir

logger = logging.getLogger('ece459')

def gitolite_creator_call(command):
    try:
        subprocess.check_call('GL_USER=p23lam gitolite ' + command,
                              shell=True,
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        msg = "command '{}' returned {}"
        logger.error(msg.format(e.cmd, e.returncode))

def is_ece459_student(username):
    command = ['gitolite', 'list-memberships', '-u', username]
    o = subprocess.check_output(command, stderr=subprocess.DEVNULL,
                                universal_newlines=True)
    for l in o.splitlines():
        if l == '@ece459-1151-students':
            return True
    return False
