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
    import pyinotify
    class EventHandler(pyinotify.ProcessEvent):
        def process_IN_CLOSE_WRITE(self, event):
            process(event.pathname)
    wm = pyinotify.WatchManager()
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    mask = pyinotify.IN_CLOSE_WRITE
    directory = os.path.join(HOME_DIR, 'testbot', 'results')
    wm.add_watch(directory, mask, rec=True)
    notifier.loop()
