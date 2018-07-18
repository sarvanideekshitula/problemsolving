# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from programming.models import Student_details, Groups
from django.views.generic import ListView
import re
# Create your views here.

def home(request):
    temp = 'programming/home.html'
    return render(request,temp,{})


def addStudent(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        codechef = request.POST.get('codechef')
        codeforces = request.POST.get('codeforces')
        year = request.POST.get('year')
        u =  Student_details(name = name, codechef = codechef, codeforces = codeforces, year = year)
        u.save()
        stu = Student_details.objects.all()
        print stu
        return HttpResponseRedirect('/programming/addstudent')
    return render(request, 'programming/addstudent.html',{})

class viewsummary(ListView):
    model = Student_details
    template_name = 'programming/viewsummary.html'

def addgroup(request):
     if request.method == 'POST':
        groupname = request.POST.get('name')
        students = request.POST.getlist('students[]')
        groupnames = Groups.objects.values_list('groupname', flat=True)
        for i in groupnames:
            if i == groupname:
                flag=0
                break
            else:
                flag=1
        if flag == 1:
            u = Groups(groupname = groupname)
            u.save()
            for i in students:
                stu = Student_details.objects.get(name = i)
                stu.groupid.add(u.id)
            return HttpResponseRedirect('/programming/addStudent')
        else:
            template = "programming/creategroup.html"
            render(request, template)
     return render(request, 'programming/creategroup.html',{'name':Student_details.objects.values_list('name', flat=True)})

def viewgroups(request):
    if request.method == 'POST':
        delstu = request.POST.getlist('delete[]')
        for i in delstu:
            stu = Groups.objects.get(groupname = i)
            stu.delete()
    return render(request, 'programming/viewgroups.html',{'groupname':Groups.objects.values_list('groupname', flat=True)})

def deleteStudents(request):
    if request.method == 'POST':
        delstu = request.POST.getlist('deletestu[]')
        for i in delstu:
            stu = Student_details.objects.get(name = i)
            stu.delete()
    return render(request, 'programming/deletestudents.html',{'stuname':Student_details.objects.values_list('name', flat=True)})

class detailGroup(ListView):
    model = Student_details
    template_name = 'programming/detailview.html'

    def get_context_data(self, **kwargs):
        context = super(detailGroup, self).get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        return context
