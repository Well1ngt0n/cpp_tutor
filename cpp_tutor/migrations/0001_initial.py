# Generated by Django 3.1.7 on 2021-04-05 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('text', models.TextField(verbose_name='Текст задачи')),
                ('difficulty', models.IntegerField(verbose_name='Сложность')),
            ],
        ),
        migrations.CreateModel(
            name='Themes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('en_name', models.TextField(verbose_name='Английское название')),
                ('theory', models.TextField(verbose_name='Теория')),
                ('link', models.TextField(default='', verbose_name='Ссылка')),
            ],
        ),
    ]
