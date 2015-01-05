# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from django_gitolite.models import Access, Repo
from django_ssh.forms import KeyForm
from django_ssh.models import Key

from emailer.models import Notification

def home(request):
    context = {'accesses': []}
    if request.user.is_authenticated():
        context['accesses'] = Access.objects.filter(user=request.user)
    return render(request, 'home.html', context)

def setup(request):
    return render(request, 'setup.html')

@login_required
def subscribe(request, repo_id):
    user = request.user
    try:
        repo = Repo.objects.get(pk=repo_id)
        Access.objects.get(repo=repo, user=user)
        Notification.objects.create(repo=repo, user=user)
    except:
        pass
    return redirect('profile')

@login_required
def unsubscribe(request, repo_id):
    try:
        repo = Repo.objects.get(pk=repo_id)
        n = Notification.objects.get(repo=repo, user=request.user)
        n.delete()
    except:
        pass
    return redirect('profile')
