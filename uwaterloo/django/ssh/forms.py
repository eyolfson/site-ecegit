# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from subprocess import check_output, CalledProcessError

from django import forms
from django.conf import settings

class KeyForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        data = self.cleaned_data['file']
        command = ['ssh-keygen', '-l', '-f', data.temporary_file_path()]
        try:
            self.output = check_output(command)
        except CalledProcessError as e:
            message = 'Please submit a valid SSH public key file.'
            raise forms.ValidationError(message, code='invalid')
        return data
