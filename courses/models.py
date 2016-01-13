# Copyright 2015-2016 Jonathan Eyolfson
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
