# Generated by Django 3.1.7 on 2021-04-19 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cpp_tutor', '0003_auto_20210419_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='themes',
            name='theory',
            field=models.TextField(default='', verbose_name='Теория'),
        ),
    ]