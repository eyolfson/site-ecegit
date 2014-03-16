import os
import math
import re
import subprocess

from functools import partial

COMMENT_PATTERN = re.compile('COMMENT: (\d+) iterations, (\d+) distance')
CLONE_URI = 'git@ecegit.uwaterloo.ca'
HOME_DIR = os.environ['HOME']
SOLVER_FILE = 'solver.cpp'
TSP_FILE = 'berlin52.tsp'
TOUR_FILE = 'berlin52.tour'
TOUR_LEN = 52

class TourException(Exception):
    pass

def compute_distances():
    coord = {}
    with open(os.path.join(HOME_DIR, TSP_FILE), 'r') as f:
        for line in f:
            if not line[0].isdigit():
                continue
            i, x, y = line.split()
            coord[int(i)] = (float(x), float(y))
    distances = {}
    for i in coord.items():
        for j in coord.items():
            if i != j:
                diff_x = i[1][0] - j[1][0]
                diff_x2 = diff_x * diff_x
                diff_y = i[1][1] - j[1][1]
                diff_y2 = diff_y * diff_y
                distances[(i[0], j[0])] = \
                    math.floor(math.sqrt(diff_x2 + diff_y2) + 0.5)
    return distances
DISTANCES = compute_distances()

def call(cwd, command):
    subprocess.check_call(command, cwd=cwd, shell=True,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.STDOUT,
                          timeout=15)

def run(repo):
    repo_dir = os.path.join(HOME_DIR, repo.rsplit('/')[-1])
    created = False
    if not os.path.exists(repo_dir):
        call(HOME_DIR, 'git clone {}:{}'.format(CLONE_URI, repo))
        created = True
    c = partial(call, repo_dir)
    if not created:
        c('git reset --hard HEAD')
        c('git pull')
    c('rm -f {}'.format(SOLVER_FILE))
    c('make clean')
    c('cp ../{0} {0}'.format(TSP_FILE))
    c('cp ../{0} {0}'.format(SOLVER_FILE))
    c('make')
    c('bin/solver {} -s 10'.format(TSP_FILE))
    return os.path.join(repo_dir, TOUR_FILE)

def validate_tour(path):
    tour = []
    matched = False
    with open(path, 'r') as f:
        for line in f:
            if not matched:
                m = COMMENT_PATTERN.match(line)
                if m:
                    iterations = int(m.group(1))
                    distance = int(m.group(2))
                    matched = True
            s = line.strip()
            if s.isdigit():
                i = int(s)
                if i in tour:
                    raise TourException('Tour has duplicate city')
                tour.append(i)
    if not matched:
        raise TourException("Tour COMMENT doesn't exist")
    if len(tour) != TOUR_LEN:
        raise TourException("Tour number of cities doesn't match")
    d = 0.0
    for i in range(1, len(tour)):
        d += DISTANCES[(tour[i], tour[i-1])]
    d += DISTANCES[(tour[0], tour[-1])]
    if abs(d - distance) > 0.1:
        raise TourException("Tour distance doesn't match")
    return (iterations, distance)

def process(path):
    print('Start', path)
    basename = os.path.basename(path)
    result_path = os.path.join(HOME_DIR, 'results', basename)
    valid = False
    with open(path, 'r') as f:
        for line in f:
            repo = line.strip()
    try:
        tour_path = run(repo)
        iterations, distance = validate_tour(tour_path)
        message = "{} iterations, {} distance".format(iterations, distance)
        valid = True
    except subprocess.CalledProcessError as e:
        message = 'Command "{}" failed'.format(e.cmd)
    except subprocess.TimeoutExpired as e:
        message = 'Command "{}" timed out'.format(e.cmd)
    except TourException as e:
        message = str(e)
    with open(result_path, 'w') as f:
        f.write('{}\n'.format(repo))
        f.write('{}\n'.format(message))
        if valid:
            f.write('{}\n'.format(iterations))
            f.write('{}\n'.format(distance))
    print('Finish', path)
    os.remove(path)

if __name__ == "__main__":
    import pyinotify
    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            process(event.pathname)
    wm = pyinotify.WatchManager()
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    mask = pyinotify.IN_CLOSE_WRITE
    directory = os.path.join(HOME_DIR, 'queue')
    wm.add_watch(directory, mask, rec=True)
    notifier.loop()
