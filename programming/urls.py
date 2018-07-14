from django.conf.urls import url, include
from programming import views
from programming.views import viewsummary

urlpatterns = [
    url(r'^$', views.addStudent, name='addstudent'),
    url(r'^viewsummary/$', viewsummary.as_view(), name='viewsummary')
]
