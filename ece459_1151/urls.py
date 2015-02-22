from django.conf.urls import patterns, url

from ece459_1151 import views

urlpatterns = patterns('',
    url(r'^(?P<slug>\w+)/$', views.assignment, name='assignment'),
)
