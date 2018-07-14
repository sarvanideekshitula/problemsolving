# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from programming.models import Groups, Student_details
# Register your models here.

admin.site.register(Student_details)
admin.site.register(Groups)
