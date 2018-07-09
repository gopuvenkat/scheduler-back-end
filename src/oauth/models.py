# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Users(models.Model):
    email = models.EmailField(unique=True)

    def __unicode__(self):
        return self.email

class Emails(models.Model):
    username = models.ForeignKey(Users, related_name='user')
    receivedDateTime = models.DateTimeField()
    title = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __unicode__(self):
        return self.title
