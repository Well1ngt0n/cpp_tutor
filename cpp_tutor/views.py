from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
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
        task = Tasks.objects.all().filter(id=task_id)
        if len(task) == 0:
            raise Http404
        task = task[0]
        voc['task'] = {'name': task.name, 'text': task.text, 'difficulty': task.difficulty}
        # voc['tests'] = ...
        return render(request, self.template_name, voc)