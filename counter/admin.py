from django.contrib import admin
from .models import Goal, Meal, Entry
# Register your models here.

myModels = [Goal, Meal, Entry]
admin.site.register(myModels)