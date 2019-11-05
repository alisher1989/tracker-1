from django.contrib.auth.models import User
from django.db import models
PROJECT_STATUS = (
    ('active', 'active'),
    ('blocked', 'blocked'),
)


def get_admin():
    return User.objects.get(username='admin').id


class Project(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name='Название проекта')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    project_status = models.CharField(max_length=20, verbose_name='Статус проекта', choices=PROJECT_STATUS, default=PROJECT_STATUS[0][0])

    def __str__(self):
        return self.name


class Task(models.Model):
    summary = models.CharField(max_length=50, null=False, blank=False, verbose_name='краткое изложение')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='описание')
    status = models.ForeignKey('webapp.Status', related_name='task_status', on_delete=models.PROTECT, null=True, blank=True, verbose_name='статус')
    type = models.ForeignKey('webapp.Type', related_name='task_type', on_delete=models.PROTECT, null=True, blank=True, verbose_name='тип')
    project = models.ForeignKey('webapp.Project', related_name='projects_task', on_delete=models.PROTECT, null=True, blank=False, verbose_name='проект')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    created_by = models.ForeignKey(User, max_length=40, null=True, blank=True, on_delete=models.PROTECT,
                               default=get_admin, verbose_name='Author', related_name='task_creator')
    assigned_to = models.ForeignKey(User, max_length=40, null=True, blank=True, on_delete=models.PROTECT,
                               default=get_admin, verbose_name='Assigned to', related_name='task_executor')

    def __str__(self):
        return self.summary


class Type(models.Model):
    type = models.CharField(max_length=50, verbose_name='тип')

    def __str__(self):
        return self.type


class Status(models.Model):
    status = models.CharField(max_length=50, verbose_name='статус')

    def __str__(self):
        return self.status