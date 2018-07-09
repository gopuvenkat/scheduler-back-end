# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from oauth.models import Users, Emails

admin.site.register(Users)
admin.site.register(Emails)
