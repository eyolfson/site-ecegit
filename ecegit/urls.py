# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'ecegit.views.home', name='home'),
    url(r'^setup/$', 'ecegit.views.setup', name='setup'),
    url(r'^profile/', include('django_ssh.urls', namespace='ssh')),
    url(r'^repo/', include('django_gitolite.urls', namespace='git')),
    url(r'^login/$', 'django_cas.views.login', name='login'),
    url(r'^logout/$', 'django_cas.views.logout', name='logout'),
    url(r'^subscribe/(?P<repo_id>\d+)/$', 'ecegit.views.subscribe',
        name='subscribe'),
    url(r'^unsubscribe/(?P<repo_id>\d+)/$', 'ecegit.views.unsubscribe',
        name='unsubscribe'),
)
