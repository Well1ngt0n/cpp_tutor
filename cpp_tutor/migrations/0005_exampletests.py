# Generated by Django 3.1.7 on 2021-04-21 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cpp_tutor', '0004_auto_20210419_2218'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExampleTests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.TextField(verbose_name='Ввод')),
                ('output', models.TextField(verbose_name='Вывод')),
                ('id_task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cpp_tutor.tasks')),
            ],
        ),
    ]
