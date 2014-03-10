import os

from ece459.models import Group, TestbotMessage, TSPResult

HOME_DIR = os.environ['HOME']

def process(path):
    print('Start', path)
    with open(path, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
    repo = lines[0]
    group = Group.objects.get(assignment__slug='a3',
                              repo__path=repo)
    TestbotMessage.objects.create(group=group,
                                  message=lines[1])
    if len(lines) == 4:
        iterations = int(lines[2])
        distance = float(lines[3])
        try:
            result = TSPResult.objects.get(group=group)
            if iterations > result.iterations:
                result.iterations = iterations
                result.distance = distance
            result.save()
        except TSPResult.DoesNotExist:
            TSPResult.objects.create(group=group,
                                     iterations=iterations,
                                     distance=distance)
    os.remove(path)
    print('Finish', path)

if __name__ == "__main__":
    from time import sleep
    while True:
        dir = '/srv/git/testbot/results'
        for basename in os.listdir(dir):
           path = os.path.join(dir, basename)
           process(path)
        sleep(1)
