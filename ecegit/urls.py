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

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'ecegit.views.home', name='home'),
    url(r'^setup/$', 'ecegit.views.setup', name='setup'),
    url(r'^commits_csv/$', 'ecegit.views.commits_csv', name='commits_csv'),
    url(r'^profile/', include('django_ssh.urls', namespace='ssh')),
    url(r'^repo/', include('django_gitolite.urls', namespace='git')),
    url(r'^login/$', 'django_cas.views.login', name='login'),
    url(r'^logout/$', 'django_cas.views.logout', name='logout'),
    url(r'^subscribe/(?P<repo_id>\d+)/$', 'ecegit.views.subscribe',
        name='subscribe'),
    url(r'^unsubscribe/(?P<repo_id>\d+)/$', 'ecegit.views.unsubscribe',
        name='unsubscribe'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ece459/1151/', include('ece459_1151.urls', namespace='ece459_1151')),
)
