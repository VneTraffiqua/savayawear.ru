from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Question, PromoPeople, Manager


@admin.register(PromoPeople)
class PromoPeople(admin.ModelAdmin):
    list_display = ['telegram_id', 'fullname']


@admin.register(Question)
class Question(admin.ModelAdmin):
    list_display = ['telegram_user_id', 'question']


@admin.register(Manager)
class Manager(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.unregister(Group)
