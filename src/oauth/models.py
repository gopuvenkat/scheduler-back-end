# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser

class Users(AbstractUser):
    class Meta:
        verbose_name_plural = "Users"

    email = models.EmailField(unique=True)
    lastchecked = models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0,0,0, 0))
    password = models.CharField(default="not_required", max_length=15)
    username = models.CharField(max_length=100, unique=True)
    def __unicode__(self):
        return self.email

class Emails(models.Model):
    class Meta:
        verbose_name_plural = "Emails"

    username = models.ForeignKey(Users, related_name='user')
    receivedDateTime = models.DateTimeField()
    title = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __unicode__(self):
        return self.title
