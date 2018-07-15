from django.conf.urls import url, include
from programming import views
from programming.views import viewsummary

urlpatterns = [
    url(r'^$', views.addStudent, name='addstudent'),
    url(r'^viewsummary/$', viewsummary.as_view(), name='viewsummary'),
    url(r'^creategroup/$', views.addgroup, name='addgroup'),
    url(r'^viewgroups/$', views.viewgroups, name='viewgroups'),
    url(r'^deletestudents/$', views.deleteStudents, name='deleteStudents'),
    url(r'^(?P<slug>[\w-]+)/$', views.detailGroup, name='detailgroup'),
]
