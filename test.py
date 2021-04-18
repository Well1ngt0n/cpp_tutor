voc = {}
task_id = 6
task = Tasks.objects.all().filter(id=task_id)
if len(task) == 0:
    raise Http404
task = task[0]
voc['task'] = {'name': task.name, 'text': task.text, 'difficulty': task.difficulty}
voc['pretests'] = []
for i in range(task.difficulty):
    try:
        pretest_in = open(f"media/tests/{task.id}/{i + 1}.in", mode='rt')
        pretest_out = open(f"media/tests/{task.id}/{i + 1}.out", mode='rt')
        voc['pretests'].append({"in": pretest_in.read(), "out": pretest_out.read()})
    except Exception:
        pass
