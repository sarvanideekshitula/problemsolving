# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from programming.models import Student_details, Groups
from django.views.generic import ListView, DetailView
import re
import os
import json
import requests
from bs4 import BeautifulSoup
# Create your views here.

def isbracket(c):
    if (c == '(' or c == '[' or c == '{' or c == '}' or c == ']' or c == ')'):
        return True
    return False

def isopposite(a,b):
    if (a == '(' and b == ')'):
        return True
    elif (a == '{' and b == '}'):
        return True
    elif (a == '[' and b == ']'):
        return True
    else:
        return False

def update(handle):
    url = "https://www.codechef.com/users/"+handle
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    script = soup.find_all('script')[36]
    startindex = script.text.find("all_rating")
    while (script.text[startindex] != '['):
        startindex = startindex + 1
    endindex = startindex + 1
    stack = ['[']
    while (len(stack) > 0):
        if (isbracket(script.text[endindex])):
            if (isopposite(stack[len(stack)-1],script.text[endindex])):
                stack.pop()
            else:
                stack.append(script.text[endindex])
        endindex = endindex + 1
    return script.text[startindex:endindex]

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

    def post(self, request, *args, **kwargs):
        handle = request.POST.get('handle')
        text = update(handle)
        u = Student_details.objects.get(codechef = handle)
        u.codechefdetails = text
        u.save()
        return HttpResponseRedirect('/programming/viewsummary')

def addgroup(request):
    if request.method == 'POST':
        groupname = request.POST.get('name')
        students = request.POST.getlist('students[]')
        u = Groups(groupname = groupname)
        u.save()
        for i in students:
            stu = Student_details.objects.get(name = i)
            stu.groupid.add(u.id)
        return HttpResponseRedirect('/programming/addStudent')
    return render(request, 'programming/creategroup.html',{'name':Student_details.objects.values_list('name',flat=True)})

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

    def get_context_data(self, *args, **kwargs):
        ctx = super(detailGroup, self).get_context_data(*args, **kwargs)
        ctx['slug'] = self.kwargs['slug'] # or Tag.objects.get(slug=...)
        return ctx

    def post(self, request, *args, **kwargs):
          delstu = request.POST.getlist('delstu[]')
          addstu = request.POST.getlist('add[]')
          grp = request.POST.get('grp')
          g = Groups.objects.get(groupname = grp)
          if len(delstu) == 0:
              for i in addstu:
                  stu = Student_details.objects.get(name = i)
                  stu.groupid.add(g.id)
          elif len(addstu) == 0:
              for i in delstu:
                  stu = Student_details.objects.get(name = i)
                  stu.groupid.remove(g.id)
          return HttpResponseRedirect('/programming/addStudent')

class studentsDetail(DetailView):
    model = Student_details
    template_name = 'programming/detailstudent.html'

    def get_context_data(self, *args, **kwargs):
        context = super(studentsDetail, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['user_info'] = Student_details.objects.get(id = pk)
        data = json.loads(context['user_info'].codechefdetails)
        rank = []
        contest = []
        rating = []
        name = []
        for key in data:
            rank.append(key['rank'])
            contest.append(key['contest'])
            rating.append(key['rating'])
            name.append(key['name'])
        context['rank'] = rank
        context['contest'] = contest
        context['rating'] = rating
        context['name'] = name
        return context
