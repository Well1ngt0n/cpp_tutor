from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Themes)
admin.site.register(Tasks)
admin.site.register(TasksConnectionThemes)
admin.site.register(ExampleTests)
admin.site.register(Verdicts)