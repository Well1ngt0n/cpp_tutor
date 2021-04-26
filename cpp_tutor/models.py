from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Themes(models.Model):
    name = models.TextField(verbose_name='Название')
    en_name = models.TextField(verbose_name='Английское название')
    theory = models.TextField(verbose_name='Теория', default='')
    link = models.TextField(verbose_name='Ссылка', default='')

    def __str__(self):
        return self.name


class Tasks(models.Model):
    name = models.TextField(verbose_name='Название')
    text = models.TextField(verbose_name='Текст задачи')
    difficulty = models.IntegerField(verbose_name='Количество претестов')  # Надо бы столбец переименовать (уже удалить)

    def __str__(self):
        return self.name


class TasksConnectionThemes(models.Model):
    id_task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    id_theme = models.ForeignKey(Themes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class ExampleTests(models.Model):
    id_task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    input = models.TextField(verbose_name='Ввод')
    output = models.TextField(verbose_name='Вывод')

    def __str__(self):
        return str(self.id)


class Verdicts(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    verdict = models.TextField(verbose_name='Вердикт', default='ok')

    def __str__(self):
        return str(self.id)
