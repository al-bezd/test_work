# -*- coding:utf-8 -*-
from django.contrib import admin
#from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse_lazy
from django.utils.translation import gettext, gettext_lazy as _
from accounts.models import User


#admin.site.unregister(User)
#from tasks.models import Task


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff','is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),

    )
#admin.site.register(User, CustomUserAdmin)

'''@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('status', 'name', 'owner_id','owner_name')
    list_display = ('id', 'name', 'viewed', 'status','args', )'''