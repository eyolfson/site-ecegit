# Copyright 2015 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.models import User
from django.db import models

from django_gitolite.models import Repo

class Course(models.Model):
    slug = models.SlugField()

    def __str__(self):
        return self.slug

class Offering(models.Model):
    course = models.ForeignKey(Course, related_name='offerings')
    term = models.PositiveSmallIntegerField()
    instructor = models.ForeignKey(User, related_name='instructor_offerings')
    staff = models.ManyToManyField(User, related_name='staff_offerings',
                                   blank=True)
    students = models.ManyToManyField(User, related_name='student_offerings',
                                      blank=True)

    def __str__(self):
        return '{}-{}'.format(self.course, self.term)

class OfferingRepo(models.Model):
    repo = models.OneToOneField(Repo, primary_key=True)
    offering = models.ForeignKey(Offering, related_name='offering_repos')
