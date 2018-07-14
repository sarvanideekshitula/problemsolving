# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from programming.models import Student_details, Groups
from django.views.generic import ListView
# Create your views here.

def addStudent(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        codechef = request.POST.get('codechef')
        codeforces = request.POST.get('codeforces')
        year = request.POST.get('year')
        u =  Student_details(name = name, codechef = codechef, codeforces = codeforces, year = year)
        u.save()
        return HttpResponseRedirect('/programming/addStudent')
    return render(request, 'programming/addstudent.html',{})

class viewsummary(ListView):
    model = Student_details
    template_name = 'programming/viewsummary.html'
