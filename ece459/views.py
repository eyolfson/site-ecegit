import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from django_gitolite.models import Repo

from ece459.models import Assignment, Group, TestbotMessage, TSPResult
from ece459.utils import gitolite_creator_call, is_ece459_student

@login_required
def assignment(request, slug):
    a = get_object_or_404(Assignment, slug=slug)
    username = request.user.username
    c = {'is_student': is_ece459_student(username),
         'tsp_results': TSPResult.objects.filter(group__assignment=a)}
    if c['is_student']:
        try:
            g = request.user.ece459_groups.get(assignment=a)
        except Group.DoesNotExist:
            g = None
        c['group'] = g
        c['testbot_messages'] = TestbotMessage.objects.filter(group=g)

    if request.method == "POST":
        if not c['is_student'] or c['group']:
            return redirect('ece459:assignment', 'a3')
        if 'partner' in request.POST:
            try:
                partner = User.objects.get(username=request.POST['username'])
            except User.DoesNotExist:
                c['register_error'] = 'Invalid partner (does not exist)'
                return render(request, 'ece459/assignment.html', c)
            if request.user == partner:
                c['register_error'] = 'Invalid partner (yourself)'
                return render(request, 'ece459/assignment.html', c)
            if not is_ece459_student(partner.username):
                c['register_error'] = 'Invalid partner'
                return render(request, 'ece459/assignment.html', c)
            try:
                partner.ece459_groups.get(assignment=a)
                c['register_error'] = 'Invalid partner (already in group)'
                return render(request, 'ece459/assignment.html', c)
            except Group.DoesNotExist:
                pass
            g = Group.objects.create(assignment=a)
            g.members.add(request.user)
            g.members.add(partner)
            r = 'ece459/1141/a3/g{}'.format(str(g.pk))
            gitolite_creator_call('fork ece459/1141/a3 {}'.format(r))
            gitolite_creator_call('perms {} + WRITERS {}'.format(r, username))
            gitolite_creator_call('perms {} + WRITERS {}'.format(r, partner.username))
            try:
                repo = Repo.objects.get(path=r)
                g.repo = repo
                g.save()
            except Repo.DoesNotExist:
                pass
            return redirect('ece459:assignment', 'a3')
        elif 'solo' in request.POST:
            g = Group.objects.create(assignment=a)
            g.members.add(request.user)
            r = 'ece459/1141/a3/g{}'.format(str(g.pk))
            gitolite_creator_call('fork ece459/1141/a3 {}'.format(r))
            gitolite_creator_call('perms {} + WRITERS {}'.format(r, username))
            try:
                repo = Repo.objects.get(path=r)
                g.repo = repo
                g.save()
            except Repo.DoesNotExist:
                pass
            return redirect('ece459:assignment', 'a3')

    return render(request, 'ece459/assignment.html', c)
