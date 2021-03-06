from concurrent.futures.process import _ThreadWakeup
from operator import mod
from statistics import mode
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

RANK_CHOICES = (
    ('Employee','EMPLOYEE'),
    ('Supervisor', 'SUPERVISOR'),
    ('Manager','Manager'),
    ('CTO','CTO'),
    ('CEO','CEO'),
    ("archive","ARCHIVE")
)


class Branches(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class Dep(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class UserDetail(models.Model):
    rank = models.CharField(max_length=100,choices=RANK_CHOICES,default="saf")
    #branch = models.CharField(max_length=100,choices=BRANCH_CHOICES,default='nasrcity')
    branch = models.ForeignKey(Branches,on_delete=models.PROTECT,related_name="users")
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='info')
    img = models.ImageField(upload_to= "files/",blank= True, null = True)
    

    def __str__(self):
        return self.user.username

class Doc(models.Model):
    name = models.CharField(max_length=300,default= "Report")
    doc = models.FileField(upload_to='files/')
    pdf = models.FileField(upload_to='files/',blank=True,null=True)
    op1 = models.FileField(upload_to='files/',blank=True,null=True)
    op2 = models.FileField(upload_to='files/',blank=True,null=True)
    coming = models.ForeignKey("UserDetail",related_name='sent',on_delete=models.PROTECT) 
    users = models.ForeignKey("UserDetail",related_name='docs',on_delete=models.PROTECT, null=True,blank=True) 
    approved = models.BooleanField(default=False)
    branch = models.ForeignKey(Branches,on_delete=models.PROTECT,related_name="docs")
    descr = models.TextField(blank=True,null=True)
    date = models.DateField(auto_now_add=True)
    sec_id = models.IntegerField(blank=True,null=True)
    created_by = models.ForeignKey(UserDetail,related_name = "created", on_delete=models.PROTECT)
    dep = models.ForeignKey(Dep,on_delete=models.PROTECT,related_name='ddocs')

    def __str__(self):
        return self.name


