# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Groups(models.Model):
    groupname = models.CharField(max_length=50)

    def __str__(self):
        return self.groupname

class Student_details(models.Model):
    name = models.CharField(max_length=50)
    codechef = models.CharField(max_length=50)
    codechefdetails = models.TextField(blank=True)
    codechefrating = models.IntegerField(default=0)
    codeforces = models.CharField(max_length=50)
    codeforcesdetails = models.TextField(blank=True)
    codeforcesrating = models.IntegerField(default=0)
    year = models.IntegerField(default=0)
    groupid = models.ManyToManyField(Groups, blank=True)

    def __str__(self):
        return self.name
