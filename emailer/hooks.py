import logging

from emailer.models import Notification

logger = logging.getLogger('emailer')

def email(push):
    notifications = Notification.objects.filter(repo=push.repo)
    notifications = notifications.exclude(user=push.user)
    if notifications.count() == 0:
        return

    BRANCH_START = 'refs/heads/'
    if not push.refname.startswith(BRANCH_START):
        return
    branch = push.refname[len(BRANCH_START):]
    if push.old_rev == '0' * 40:
        return
    if push.new_rev == '0' * 40:
        return

    from email.header import Header
    from email.mime.text import MIMEText
    from subprocess import check_output, Popen, PIPE, CalledProcessError

    try:
        o = check_output(['git',
            '--git-dir=/srv/git/repositories/{}.git'.format(push.repo.path),
            'log', '--stat', '{}..{}'.format(push.old_rev, push.new_rev)])
    except CalledProcessError as e:
        msg = "command '{}' returned {}"
        logger.error(msg.format(' '.join(e.cmd), e.returncode))
        return

    msg = MIMEText(o.decode('utf-8'))
    msg['From'] = 'Git <git@ecegit.uwaterloo.ca>'
    msg['Subject'] = '[{}] {} branch updated by {}'.format(push.repo.path,
                                                           branch,
                                                           push.user.username)
    msg['X-Git-Host'] = 'ecegit.uwaterloo.ca'
    msg['X-Git-Repo'] = push.repo.path
    msg['X-Git-Refname'] = push.refname
    msg['X-Git-Reftype'] = 'branch'
    for notification in notifications:
        msg['To'] = '{}@uwaterloo.ca'.format(notification.user.username)
        try:
            p = Popen(['sendmail', '-oi', '-t'], stdin=PIPE, universal_newlines=True)
            p.communicate(str(msg))
        except CalledProcessError as e:
            msg = "command '{}' returned {}"
            logger.error(msg.format(' '.join(e.cmd), e.returncode))
        del msg['To']
