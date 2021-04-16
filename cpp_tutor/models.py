from django.db import models


# Create your models here.

class Themes(models.Model):
    name = models.TextField(verbose_name='Название')
    en_name = models.TextField(verbose_name='Английское название')
    theory = models.TextField(verbose_name='Теория')
    link = models.TextField(verbose_name='Ссылка', default='')

    def __str__(self):
        return self.name


class Tasks(models.Model):
    name = models.TextField(verbose_name='Название')
    text = models.TextField(verbose_name='Текст задачи')
    difficulty = models.IntegerField(verbose_name='Сложность')

    def __str__(self):
        return self.name


class TasksConnectionThemes(models.Model):
    id_task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    id_theme = models.ForeignKey(Themes, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
