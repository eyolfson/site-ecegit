# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from subprocess import call, check_output, DEVNULL

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from eyl.django.gitolite.models import Access, Push, Repo

class Command(BaseCommand):
    args = '<name [path [username operation]]>'
    help = 'Handles gitolite triggers'

    def handle(self, name, *args, **options):
        if not len(args) in (0, 1, 3):
            raise CommandError('Invalid number of arguments.')
        if len(args) == 1:
            path, = args
        if len(args) == 3:
            path, username, operation = args

        if name == 'POST_COMPILE':
            output = check_output(['gitolite', 'list-phy-repos'],
                                  stderr=DEVNULL)
            repo_paths = [x.decode('utf-8') for x in output.splitlines()]
            for path in repo_paths:
                repo, created = Repo.objects.get_or_create(path)
                # Ensure the repo is synced with gitolite
                if not created:
                    repo.sync()
                    repo.save()
                Access.objects.filter(repo=repo).delete()
                for user in get_user_model().objects.all():
                    if not call(['gitolite', 'access', '-q', path,
                                 user.username, 'R']):
                        Access.objects.create(repo=repo, user=user)
