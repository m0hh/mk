from operator import mod
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

RANK_CHOICES = (
    ('saf','SAF'),
    ('zabet', 'ZABET'),
    ('superzabet','SUPERZABET'),
    ('modeer','MODEER'),
    ('raeesarkan','RAEESARKAN'),
)
"""BRANCH_CHOICES = (
    ('ramsees','RAMSEES'),
    ('nasrcity', 'NASRCITY'),
    ('tagamo3','TAGAMO3'),
    ("modeer","MODEER"),
    ('raeesarkan','RAEESARKAN'),
)"""

class Branches(models.Model):
    name = models.CharField(max_length=400)

    def __str__(self):
        return self.name


class UserDetail(models.Model):
    rank = models.CharField(max_length=100,choices=RANK_CHOICES,default='saf')
    #branch = models.CharField(max_length=100,choices=BRANCH_CHOICES,default='nasrcity')
    branch = models.ForeignKey(Branches,on_delete=models.PROTECT,related_name="users")
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='info')

    def __str__(self):
        return self.user.username

class Doc(models.Model):
    name = models.CharField(max_length=300,default= "Report")
    doc = models.FileField(upload_to='files/')
    op1 = models.FileField(upload_to='files/',blank=True,null=True)
    op2 = models.FileField(upload_to='files/',blank=True,null=True)
    coming = models.ForeignKey("UserDetail",related_name='sent',on_delete=models.PROTECT) 
    users = models.ForeignKey("UserDetail",related_name='docs',on_delete=models.PROTECT) 
    approved = models.BooleanField(default=False)
    #branch = models.CharField(max_length=100,choices=BRANCH_CHOICES)
    branch = models.ForeignKey(Branches,on_delete=models.PROTECT,related_name="docs")
    descr = models.TextField(blank=True,null=True)
    date = models.DateField(auto_now_add=True)
    sec_id = models.IntegerField(blank=True,null=True)
    created_by = models.ForeignKey(UserDetail,related_name = "created", on_delete=models.PROTECT)
    def __str__(self):
        return self.name


