#coding:utf8
'''
from django.contrib.auth.models import User, UserManager, AbstractUser
from django.db import models

from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from tasks.models import Task

User.admin_auth=reverse_lazy('admin_auth',kwargs={'account':User.username})

'''
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass
    '''
    my_task=models.ManyToManyField(Task,blank=True,verbose_name="Мои задания")

    def admin_auth(self):
        return reverse_lazy('admin_auth', kwargs={'account': self.username})

    def admin_auth_url(self):
        url=reverse_lazy('accounts:admin_auth', kwargs={'account': self.username})
        return mark_safe('<a href="%s">Авторизоваться от имени %s</a>'%(url, self.username))

    def get_task(self,id):
        return Task.objects.get(id=id)'''

