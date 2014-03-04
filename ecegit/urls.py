# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'ecegit.views.home', name='home'),
    url(r'^setup/$', 'ecegit.views.setup', name='setup'),
    url(r'^profile/$', 'ecegit.views.profile', name='profile'),
    url(r'^profile/(?P<key_id>\d+)/$', 'ecegit.views.profile_remove',
        name='profile_remove'),
    url(r'^login/$', 'django_cas.views.login', name='login'),
    url(r'^logout/$', 'django_cas.views.logout', name='logout'),
    url(r'^ece459/', include('ece459.urls', namespace="ece459")),
)
