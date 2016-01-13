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

import os
import re

from collections import namedtuple
from subprocess import check_output, STDOUT, CalledProcessError

class Version(namedtuple('Version', ['major', 'minor', 'patch', 'extra'])):

    def __str__(self):
        s = '{}.{}.{}'.format(self.major, self.minor, self.patch)
        if self.extra:
            return '{}-{}'.format(s, self.extra)
        return s

def get_version():
    version = Version(0, 0, 1, '')

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    GIT_DIR = os.path.join(BASE_DIR, '.git')
    if not os.path.isdir(GIT_DIR):
        return version

    try:
        output = check_output(['git', '--git-dir={}'.format(GIT_DIR),
                               '--work-tree={}'.format(BASE_DIR),
                               'describe', '--abbrev=6', '--match', 'v*',
                               '--dirty=-dirty'], stderr=STDOUT)
    except CalledProcessError:
        return version

    output = output.strip().decode()
    match = re.match('v([0-9]+)\.([0-9]+)\.([0-9]+)-(.*)', output)
    if not match:
        return version
    return Version(int(match.group(1)), int(match.group(2)),
                   int(match.group(3)), match.group(4))
