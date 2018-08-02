# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from programming.models import Student_details, Groups
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from programming.forms import StudentForm, GroupForm
import re
import os
import json
import requests
from bs4 import BeautifulSoup
from django.urls import reverse_lazy
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
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36\(KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    soup = BeautifulSoup(r.content, 'html.parser')
    print soup
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

def getUserRating(handlename):
	res = requests.get('http://codeforces.com/api/user.rating?handle='+handlename)
	return res.text

def home(request):
    temp = 'programming/home.html'
    return render(request,temp,{})

class StudentView(CreateView):
    form_class = StudentForm
    template_name = 'programming/addstudent.html'
    success_url = reverse_lazy('home')

class viewsummary(ListView):
    model = Student_details
    template_name = 'programming/viewsummary.html'

    def post(self, request, *args, **kwargs):
        codechef = request.POST.get('codechef')
        codeforces = request.POST.get('codeforces')
        codecheftext = update(codechef)
        codeforcestext = getUserRating(codeforces)
        u = Student_details.objects.get(codechef = codechef)
        u.codechefdetails = codecheftext
        u.codeforcesdetails = codeforcestext
        u.save()
        return HttpResponseRedirect('/programming/viewsummary')

class addGroup(CreateView):
    form_class = GroupForm
    template_name = 'programming/creategroup.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        ctx = super(addGroup, self).get_context_data(*args, **kwargs)
        ctx['name'] = Student_details.objects.values_list('name', flat=True)
        return ctx

    def post(self, request, *args, **kwargs):
        students = request.POST.getlist('students[]')
        groupname = request.POST.get('groupname')

        for i in students:
            stu = Student_details.objects.get(name = i)
            stu.groupid.add(Groups.objects.get(groupname = groupname).id)


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
          grp = request.POST.get('groupname')
          g = Groups.objects.get(groupname = grp)
          if len(delstu) == 0:
              for i in addstu:
                  stu = Student_details.objects.get(name = i)
                  stu.groupid.add(g.id)
          elif len(addstu) == 0:
              for i in delstu:
                  stu = Student_details.objects.get(name = i)
                  stu.groupid.remove(g.id)
          return HttpResponseRedirect('/programming/detailgroup/%s'%g.groupname)

class studentsDetail(DetailView):
    model = Student_details
    template_name = 'programming/detailstudent.html'

    def get_context_data(self, *args, **kwargs):
        context = super(studentsDetail, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['user_info'] = Student_details.objects.get(id = pk)
        codechefdata = json.loads(context['user_info'].codechefdetails)
        codeforcesdata = json.loads(context['user_info'].codeforcesdetails)
        context['user_info'].codechefrating = codechefdata[len(codechefdata)-1]['rating']
        context['user_info'].codeforcesrating = codeforcesdata['result'][len(codeforcesdata['result'])-1]['newRating']
        context['user_info'].save()
        context['ranks'] = reversed(codechefdata)
        context['codeforcesrank'] = reversed(codeforcesdata['result'])
        return context
