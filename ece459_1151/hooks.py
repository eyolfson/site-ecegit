import os

from subprocess import call

from django_gitolite.utils import home_dir

from ece459.models import Group

def testbot(push):
    try:
        group = Group.objects.get(repo=push.repo, assignment__slug='a3')
    except Group.DoesNotExist:
        return
    if push.refname != 'refs/heads/master':
        return
    try:
        filename = os.path.join('/home/ece459/queue', str(push.pk))
        with open(filename, 'w') as f:
            f.write(str(push.repo))
            f.write('\n')
        rc = call(['scp', filename, 'ece459@costa.cs.uwaterloo.ca:queue'])
        if rc == 0:
            os.remove(filename)
    except:
        print('[testbot] error, this push was not added to the queue')
