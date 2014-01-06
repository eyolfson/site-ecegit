# Copyright 2014 Jon Eyolfson
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from uwaterloo.django.ssh.forms import KeyForm

def home(request):
    return render(request, 'home.html')

@login_required
def profile(request):
    if request.method == 'POST':
        form = KeyForm(request.POST, request.FILES)
        if form.is_valid():
            return redirect('profile')
    else:
        form = KeyForm()
    return render(request, 'profile.html', {'form': form})
