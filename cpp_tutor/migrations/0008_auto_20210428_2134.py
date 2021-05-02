# Generated by Django 3.1.7 on 2021-04-28 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpp_tutor', '0007_verdicts_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='verdicts',
            name='correct_out',
            field=models.TextField(default='', verbose_name='Правильный ответ'),
        ),
        migrations.AddField(
            model_name='verdicts',
            name='input',
            field=models.TextField(default='', verbose_name='Ввод'),
        ),
        migrations.AddField(
            model_name='verdicts',
            name='output',
            field=models.TextField(default='', verbose_name='Вывод'),
        ),
    ]
