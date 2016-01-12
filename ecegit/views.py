# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
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
def commits_csv(request):
    if not request.user.username in ['jeyolfso', 'drayside', 'a3zaman']:
        return HttpResponseForbidden()

    from .forms import CommitTimeForm

    if request.method == 'POST':
        form = CommitTimeForm(request.POST)
        if form.is_valid():
            timestamp = form.cleaned_data['timestamp']
            # timestamp = timezone('US/Eastern').localize(form.cleaned_data['timestamp'])
            import csv
            from django_gitolite.models import Push
            from subprocess import check_output

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="commits.csv"'
            writer = csv.writer(response)

            students = [x.decode() for x in check_output(['gitolite', 'list-members', '@ece351-1161-students']).splitlines()]
            for student in students:
                pushes = Push.objects.filter(user__username=student,
                                 repo__path='ece351/1161/{}/labs'.format(student),
                                 time__lte=timestamp, refname='refs/heads/master').order_by('-time')
                if pushes.count() > 0:
                    rev = pushes[0].new_rev
                else:
                    rev = '0000000000000000000000000000000000000000'
                writer.writerow([student, rev])
            return response
    else:
        form = CommitTimeForm()
    return render(request, 'commits_csv.html', {'form': form})

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
