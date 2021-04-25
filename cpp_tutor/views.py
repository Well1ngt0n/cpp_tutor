import os
from zipfile import ZipFile

import requests
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *


# Create your views here.
class Index(TemplateView):
    template_name = 'cpp_tutor/index.html'

    def get(self, request):
        try:
            login = request.session['login']
        except KeyError:
            login = False
        return render(request, self.template_name, {'login': login})


def handler(request):
    action = request.POST['action']
    ans = {}
    if action == 'auth':
        try:
            user = User.objects.all().filter(username=request.POST['login'])
            if len(user) == 0:
                raise ValueError("Пользователя с таким логинов не существует")
            user = user[0]
            if not check_password(request.POST['password'], user.password):
                raise ValueError("Неверный пароль")
            request.session['login'] = user.username
            ans = {'answer': 'success'}
        except ValueError as e:
            ans = {'answer': 'error', 'error': str(e)}
    elif action == 'reg':
        try:
            user = User.objects.all().filter(username=request.POST['login'])
            if len(user) != 0:
                raise ValueError("Логин занят")
            user = User(username=request.POST['login'], password=make_password(request.POST['password']),
                        email=request.POST['email'])
            user.save()
            ans = {'answer': 'success'}
        except ValueError as e:
            ans = {'answer': 'error', 'error': str(e)}
    elif action == 'exit':
        request.session['login'] = False
        ans = {'answer': 'success'}
    elif action == "run-code":
        json = {
            "clientId": "7e55c29eddf75a8fabf054631513393d",
            "clientSecret": "377ab0321a1d2b9f8f6db8f04e0b9174b61ab3424cb741899fb5ef508c43eaf5",
            "script": request.POST['script'],
            "stdin": request.POST['inpt'],
            "language": "cpp17",
            "versionIndex": 0
        }
        ans = requests.post("https://api.jdoodle.com/v1/execute", json=json).json()
        if 'error' in ans:
            return JsonResponse({'answer': 'error', 'error': ans['error']})
        else:
            return JsonResponse({'answer': 'ok', 'output': ans['output']})

    elif action == "check-task":
        json = {
            "clientId": "7e55c29eddf75a8fabf054631513393d",
            "clientSecret": "377ab0321a1d2b9f8f6db8f04e0b9174b61ab3424cb741899fb5ef508c43eaf5",
            "script": request.POST['script'],
            "stdin": '',
            "language": "cpp17",
            "versionIndex": 0
        }
        lst = []

        task_id = int(request.POST['id_task'])
        for test in os.listdir(f'media/tests/{task_id}'):
            name, in_out = test.split('.')
            if in_out == "in" and os.access(f'media/tests/{task_id}/{name}.out', os.R_OK):

                with open(f'media/tests/{task_id}/{test}', mode='rt', encoding='utf-8') as file:
                    json['stdin'] = ''.join(file.readlines())

                ans = requests.post('https://api.jdoodle.com/v1/execute', json=json).json()

                if 'error' in ans:
                    lst.append("Error")
                    return JsonResponse({'tests': lst, 'verdict': f'Error on test {len(lst)}'})
                    # Потом можно расширить и написать какая именно ошибка вылетает
                else:
                    with open(f'media/tests/{task_id}/{name}.out', mode='rt', encoding='utf-8') as output:
                        # Нужно привести корректный вывод в читаемое состояние
                        # Вообще, в более сложных задачах это, наверно не прокатит
                        # Но пока попробуем так, времени то нет
                        out = output.read().split('\n')
                        for i in range(len(out)):
                            s = out[i].split()
                            for j in range(len(s)):
                                try:
                                    s[j] = str(float(s[j]))
                                except Exception:
                                    pass
                            out[i] = ' '.join(s)
                        while out[-1] == '':
                            # Я не знаю зачем на конце файлов .out пустые строки, приходится избавляться
                            out.pop()
                        # Как же я, бл@н, намучался с этим форматом
                        # Вот тут начинаем проверочку, а еще только начинаю, а ведь еще уроки делать...
                        fl = True
                        out_p = ans['output'].split('\n')
                        out_p = [i.split() for i in out_p]
                        out = [i.split() for i in out]
                        if len(out) != len(out_p):
                            fl = False
                        else:
                            for i in range(len(out)):
                                if len(out[i]) != len(out_p[i]):  # Разное количество строк
                                    fl = False
                                    break
                                else:
                                    # Этот формат записи числа выдает false при isdecimal...
                                    # Как же я уже задолбался дебажить....
                                    for j in range(len(out[i])):
                                        try:
                                            if float(out[i][j]) != float(out_p[i][j]):
                                                fl = False
                                                break
                                        except Exception:
                                            if out[i][j] != out_p[i][j]:
                                                fl = False
                                                break
                        if fl:  # Нужно потестить будет все то, что сверху
                            lst.append('ok')
                        else:
                            lst.append('wa')
                            Verdicts(id_task=Tasks.objects.all().filter(id=task_id)[0],
                                     id_user=User.objects.all().filter(username=request.session['login'])[0],
                                     verdict='error').save()

                            return JsonResponse({'tests': lst,
                                                 'verdict': f'wrong answer test {len(lst)}',
                                                 'input_p': json['stdin'],
                                                 'output_p': ans['output'],
                                                 'correct_output': '\n'.join(
                                                     [' '.join(out[i]) for i in range(len(out))]),
                                                 })
        Verdicts(id_task=Tasks.objects.all().filter(id=task_id)[0],
                 id_user=User.objects.all().filter(username=request.session['login'])[0], verdict='ok').save()
        return JsonResponse(
            {'tests': lst, 'verdict': 'complete solution', 'tests_count': len(os.listdir(f'media/tests/{task_id}'))})
    return JsonResponse(ans)


class ThemesView(TemplateView):
    template_name = 'cpp_tutor/themes.html'

    def get(self, request):
        voc = {}
        try:
            voc['login'] = request.session['login']
        except KeyError:
            voc['login'] = False
        themes = Themes.objects.all()
        voc['themes'] = []
        for theme in themes:
            voc['themes'].append({'name': theme.name, 'en': theme.en_name, 'theory': theme.theory, 'link': theme.link})
        return render(request, self.template_name, voc)


class ThemeView(TemplateView):
    template_name = 'cpp_tutor/theme.html'

    def get(self, request, theme_name):
        voc = {}
        try:
            voc['login'] = request.session['login']
            user = User.objects.all().filter(username=voc['login'])[0]
        except KeyError:
            voc['login'] = False
        theme = Themes.objects.all().filter(link=theme_name)
        if len(theme) == 0:
            raise Http404
        theme = theme[0]
        tasks = TasksConnectionThemes.objects.all().filter(id_theme=theme.id)
        voc['tasks'] = []
        for task in tasks:
            voc['tasks'].append({'id': task.id_task.id, 'name': task.id_task.name, 'complete': False})
            if voc['login']:
                complete = Verdicts.objects.all().filter(id_task=task.id_task, id_user=user, verdict='ok')
                if len(complete) > 0:
                    voc['tasks'][-1]['complete'] = True

        voc['theme'] = {'theory': theme.theory, 'name': theme.name, 'link': theme.link}
        return render(request, self.template_name, voc)


class TaskView(TemplateView):
    template_name = 'cpp_tutor/task.html'

    def get(self, request, task_id):
        voc = {}
        try:
            voc['login'] = request.session['login']
            user = User.objects.all().filter(username=voc['login'])[0]
        except KeyError:
            voc['login'] = False
        voc['cur'] = task_id
        task = Tasks.objects.all().filter(id=task_id)
        if len(task) == 0:
            raise Http404
        task = task[0]
        voc['task'] = {'id': task_id, 'name': task.name, 'text': task.text, 'difficulty': task.difficulty}
        voc['pretests'] = []
        for i in range(task.difficulty):
            try:
                pretest_in = open(f"media/tests/{task.id}/{i + 1}.in", mode='rt')
                pretest_out = open(f"media/tests/{task.id}/{i + 1}.out", mode='rt')
                voc['pretests'].append({"in": pretest_in.read(), "out": pretest_out.read()})
            except Exception:
                pass
        theme = TasksConnectionThemes.objects.all().filter(id_task=task_id)
        if len(theme) == 0:
            raise Http404
        theme = theme[0].id_theme
        voc['theme'] = {'name': theme.name, 'link': theme.link}
        tasks = TasksConnectionThemes.objects.all().filter(id_theme=theme.id)
        voc['tasks'] = []
        for task in tasks:
            voc['tasks'].append({'id': task.id_task.id, 'name': task.id_task.name, 'complete': False})
            if voc['login']:
                complete = Verdicts.objects.all().filter(id_task=task.id_task, id_user=user, verdict='ok')
                if len(complete) > 0:
                    voc['tasks'][-1]['complete'] = True
        return render(request, self.template_name, voc)


def upload_task(request):
    template_name = 'cpp_tutor/upload_task.html'
    voc = {}
    try:
        voc['login'] = request.session['login']
        cur_user = User.objects.all().filter(username=request.session['login'])[0]
        voc['admin'] = cur_user.is_superuser
    except Exception:
        voc['login'] = voc['admin'] = False
    if request.method == "POST" and request.FILES['archive']:
        file = request.FILES['archive']
        if file.name.split('.')[-1] == 'zip':
            fs = FileSystemStorage(location='media/zip_examples')
            fs.save('archive.zip', file)
            with ZipFile('media/zip_examples/archive.zip') as zipfile:
                i = 1
                for test in zipfile.namelist():
                    in_out = test.split('.')[-1]
                    if in_out in ("in", "out"):
                        task_id = Tasks.objects.latest("id").id + 1
                        try:
                            os.mkdir(f'media/tests/{task_id}')
                        except Exception:
                            pass
                        test_write = open(f'media/tests/{task_id}/{i}.{in_out}', 'w+')
                        test_file = zipfile.open(test, mode='r').read().decode('utf-8')
                        test_write.write(test_file)
                        test_write.close()
                        if in_out == "out":
                            i += 1
            os.remove('media/zip_examples/archive.zip')
            new_task = Tasks(name=request.POST['name'], text=request.POST['text'],
                             difficulty=0)
            new_task.save()
            cnt = 0
            for i in range(int(request.POST['num-example-tests'])):
                ExampleTests(id_task=new_task, input=request.POST['input' + str(i + 1)],
                             output=request.POST['output' + str(i + 1)]).save()
                cnt += 1
            voc['error'] = 'Загрузка задачи прошла успешно'
        else:
            voc['error'] = 'Архив не в расширении .zip'
    return render(request, template_name, voc)
