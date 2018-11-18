# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from programming.models import Student_details, Groups, DailyChallenges
from django.views.generic import ListView, DetailView, DeleteView, CreateView, TemplateView
from programming.forms import StudentForm, GroupForm, DailyChallengesForm
import re
import os
import json
import requests
import csv
from bs4 import BeautifulSoup
from programming.programing import update, getUserRating, dailychallengeupdate, dailychallengedata
from django.urls import reverse_lazy
from django.db.models import Avg
# Create your views here.

class home(TemplateView):
    template_name = 'programming/home.html'
    def get_context_data(self, *args, **kwargs):
        ctx = super(home, self).get_context_data(*args, **kwargs)
        ctx['averagecodechef'] = Student_details.objects.all().aggregate(Avg('codechefrating'))
        ctx['averagecodechef'] = round(ctx['averagecodechef']['codechefrating__avg'],2)
        ctx['averagecodeforces'] = Student_details.objects.all().aggregate(Avg('codeforcesrating'))
        ctx['averagecodeforces'] = round(ctx['averagecodeforces']['codeforcesrating__avg'],2)
        ctx['averagedailyproblemssolved'] = DailyChallenges.objects.all().aggregate(Avg('count'))
        ctx['averagedailyproblemssolved'] = round(ctx['averagedailyproblemssolved']['count__avg'],2)
        return ctx

class StudentView(CreateView):
    model = Student_details
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

def addgroup(request):
    if request.method == 'POST':
        groupname = request.POST.get('name')
        students = request.POST.getlist('students[]')
        u = Groups(groupname = groupname)
        u.save()
        for i in students:
            stu = Student_details.objects.get(name = i)
            stu.groupid.add(u.id)
        return HttpResponseRedirect('/programming/')
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
        ctx['codechef'] = Student_details.objects.all().order_by('-codechefrating')
        ctx['codeforces'] = Student_details.objects.all().order_by('-codeforcesrating')
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
        link = "/programming/detailgroup/" + grp
        return HttpResponseRedirect(link)

class studentsDetail(DetailView):
    model = Student_details
    template_name = 'programming/detailstudent.html'

    def get_context_data(self, *args, **kwargs):
        context = super(studentsDetail, self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        context['user_info'] = Student_details.objects.get(id = pk)
        data = dailychallengedata(context['user_info'].codeforces)
        dailychallenges = DailyChallenges.objects.values_list('probname', flat=True)
        challenges = {}
        for i in dailychallenges:
            for j in data['result']:
                if(j['problem']['name'] == i):
                    challenge = i
                    challenges[challenge] = 'Yes'
                    break
                else:
                    challenge = i
                    challenges[challenge] = 'No'
        context['solved'] = challenges
        codechefdata = json.loads(context['user_info'].codechefdetails)
        codeforcesdata = json.loads(context['user_info'].codeforcesdetails)
        context['user_info'].codechefrating = codechefdata[len(codechefdata)-1]['rating']
        context['user_info'].codeforcesrating = codeforcesdata['result'][len(codeforcesdata['result'])-1]['newRating']
        context['user_info'].save()
        context['ranks'] = codechefdata
        context['codeforcesrank'] = codeforcesdata['result']
        return context


class dailyChallenges(CreateView):
    model = DailyChallenges
    form_class = DailyChallengesForm
    template_name = 'programming/dailychallenges.html'
    success_url = reverse_lazy('searchDailyChallenges')

class searchDailyChallenges(ListView):
    form_class = DailyChallengesForm
    model = DailyChallenges
    template_name = 'programming/searchdailychallenge.html'

    def post(self, request, *args, **kwargs):
        proname = request.POST.get('proname')
        proname1 = DailyChallenges.objects.get(probname = proname)
        allstu = Student_details.objects.all()
        names = {}
        cnt = 0
        for i in allstu:
            name = i.name
            value = dailychallengeupdate(i.codeforces, proname)
            names[name] = value
            if(value):
                cnt = cnt + 1
        proname1.count = cnt
        proname1.save()
        return render(request, self.template_name, {'names':names})

def upload(request):
    with open("programming/text.csv") as f:
        reader = csv.reader(f)
        for row in reader:
            created = Student_details.objects.get_or_create(name=row[0], codechef=row[1], codeforces=row[2], year=int(row[3]))
    return HttpResponseRedirect('/programming/addstudent')
