from django.conf.urls import patterns, url

from ece459 import views

urlpatterns = patterns('',
    url(r'^1141/(?P<slug>\w+)/$', views.assignment, name='assignment'),
)
