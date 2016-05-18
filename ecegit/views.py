# Copyright 2014-2016 Jonathan Eyolfson
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

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
    if not request.user.username in ['jeyolfso', 'drayside', 'a3zaman',
                                     'rbabaeec', 'j4bian', 'dhshin',
                                     'talguind']:
        return HttpResponseForbidden()

    from .forms import CommitTimeForm

    if request.method == 'POST':
        form = CommitTimeForm(request.POST)
        if form.is_valid():
            term = str(form.cleaned_data['term'])
            timestamp = form.cleaned_data['timestamp']
            # timestamp = timezone('US/Eastern').localize(form.cleaned_data['timestamp'])
            import csv
            from django_gitolite.models import Push
            from subprocess import check_output

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="commits.csv"'
            writer = csv.writer(response)

            students_group = '@ece351-{}-students'.format(term)
            students = [x.decode() for x in check_output(['gitolite', 'list-members', students_group]).splitlines()]
            for student in students:
                student_repo_path = 'ece351/{}/{}/labs'.format(term, student)
                pushes = Push.objects.filter(user__username=student,
                                 repo__path=student_repo_path,
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
