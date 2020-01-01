from django.db import models

# Create your models here.
#from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
from django.urls import reverse
from django.urls import reverse_lazy

from accounts.models import User


class Post(models.Model):
    title       = models.CharField(max_length=128)
    body        = RichTextField()
    author      = models.ForeignKey(User,on_delete=True)
    data_create = models.DateTimeField(auto_now_add=True)
    comment     = models.TextField(blank=True,null=True)
    enable      = models.BooleanField()

    def __str__(self):
        return "%s"%self.title

    def url(self):
        return reverse_lazy("accounts:detail_post",kwargs={'pk': self.pk})

    def short_view(self):
        return "%s..."%self.body[0:50]
