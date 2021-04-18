import os
from zipfile import ZipFile

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
        return JsonResponse(ans)
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
        except KeyError:
            voc['login'] = False
        theme = Themes.objects.all().filter(link=theme_name)
        if len(theme) == 0:
            raise Http404
        theme = theme[0]
        tasks = TasksConnectionThemes.objects.all().filter(id_theme=theme.id)
        voc['tasks'] = []
        for task in tasks:
            voc['tasks'].append({'id': task.id_task.id, 'name': task.id_task.name})
        voc['theme'] = {'theory': theme.theory, 'name': theme.name}
        return render(request, self.template_name, voc)


class TaskView(TemplateView):
    template_name = 'cpp_tutor/task.html'

    def get(self, request, task_id):
        voc = {}
        try:
            voc['login'] = request.session['login']
        except KeyError:
            voc['login'] = False
        voc['cur'] = task_id
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
        theme = TasksConnectionThemes.objects.all().filter(id_task=task_id)
        if len(theme) == 0:
            raise Http404
        theme = theme[0].id_theme
        voc['theme'] = {'name': theme.name, 'link': theme.link}
        tasks = TasksConnectionThemes.objects.all().filter(id_theme=theme.id)
        voc['tasks'] = []
        for task in tasks:
            voc['tasks'].append({'id': task.id_task.id, 'name': task.id_task.name})
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
                             difficulty=request.POST['num-example-tests'])
            new_task.save()
            voc['error'] = 'Загрузка задачи прошла успешно'
        else:
            voc['error'] = 'Архив не в расширении .zip'
    return render(request, template_name, voc)
