# Copyright 2015 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from courses.models import Course, Offering

admin.site.register(Course)
admin.site.register(Offering)
