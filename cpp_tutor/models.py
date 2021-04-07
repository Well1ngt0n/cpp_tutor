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
