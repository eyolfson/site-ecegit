# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from subprocess import check_output, Popen, DEVNULL, PIPE

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from eyl.django.gitolite.models import Access, Push, Repo

class Command(BaseCommand):
    args = '<name [path [username operation]]>'
    help = 'Handles gitolite triggers'

    def handle(self, name, *args, **options):
        if name == 'POST_COMPILE':
            if len(args) != 0:
                raise CommandError('Invalid number of arguments for POST_COMPILE.')
            self.post_compile()
        elif name == 'POST_CREATE':
            if not len(args) in (1, 3):
                raise CommandError('Invalid number of arguments for POST_CREATE.')
            if len(args) == 1:
                # This is just a normal create, it'll be handled by POST_COMPILE
                return
            self.post_create(*args)

    def repo_clean(self, path):
        repo, created = Repo.objects.get_or_create(path)
        # Ensure the repo is synced with gitolite
        if not created:
            repo.sync()
            repo.save()
        Access.objects.filter(repo=repo).delete()
        return repo

    def post_compile(self):
        output = check_output(['gitolite', 'list-phy-repos'], stderr=DEVNULL)
        repo_paths = [x.decode() for x in output.splitlines()]
        repo_list = [self.repo_clean(x) for x in repo_paths]
        user_list = list(get_user_model().objects.all())
        with Popen(['gitolite', 'access', '%', '%', 'R', 'any'],
                   stdin=PIPE, stdout=PIPE, stderr=DEVNULL,
                   universal_newlines=True) as p:

            for repo in repo_list:
                for user in user_list:
                    p.stdin.write(repo.path)
                    p.stdin.write(' ')
                    p.stdin.write(user.username)
                    p.stdin.write('\n')
            p.stdin.close()

            access_list = []
            i = repo_list.__iter__()
            j = user_list.__iter__()
            repo = next(i)
            for line in p.stdout:
                ret = line.strip().split('\t')[2]
                try:
                    user = next(j)
                except StopIteration:
                    j = user_list.__iter__()
                    repo = next(i)
                    user = next(j)
                if not ret.startswith('DENIED'):
                    access_list.append(Access(repo=repo, user=user))
                if len(access_list) > 100:
                    Access.objects.bulk_create(access_list)
                    access_list = []
            if len(access_list) != 0:
                Access.objects.bulk_create(access_list)

    def post_create(self, path, username, operation):
        repo = self.repo_clean(path)
        user_list = list(get_user_model().objects.all())
        with Popen(['gitolite', 'access', repo.path, '%', 'R', 'any'],
                   stdin=PIPE, stdout=PIPE, stderr=DEVNULL,
                   universal_newlines=True) as p:

            for user in user_list:
                p.stdin.write(user.username)
                p.stdin.write('\n')
            p.stdin.close()

            access_list = []
            j = user_list.__iter__()
            for line in p.stdout:
                ret = line.strip().split('\t')[2]
                user = next(j)
                if not ret.startswith('DENIED'):
                    access_list.append(Access(repo=repo, user=user))
                if len(access_list) > 100:
                    Access.objects.bulk_create(access_list)
                    access_list = []
            if len(access_list) != 0:
                Access.objects.bulk_create(access_list)
