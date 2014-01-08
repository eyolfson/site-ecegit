# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'uwaterloo.git.django.views.home', name='home'),
    url(r'^setup/$', 'uwaterloo.git.django.views.setup', name='setup'),
    url(r'^profile/$', 'uwaterloo.git.django.views.profile', name='profile'),
    url(r'^profile/(?P<key_id>\d+)/$',
        'uwaterloo.git.django.views.profile_remove', name='profile_remove'),
    url(r'^login/$', 'uwaterloo.django.cas.views.login', name='login'),
    url(r'^logout/$', 'uwaterloo.django.cas.views.logout', name='logout'),
)
