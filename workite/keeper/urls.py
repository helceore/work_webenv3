# -*- coding: utf-8 -*-
"""workite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.conf.urls import url

from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

app_name = 'keeper'

urlpatterns = [
    # url(r'^1/', views.basic_one),
    url(r'^test_select/', views.test_select),
    url(r'^keepermarkeredit/', views.keepermarker),
    url(r'^keepermarkeredit_add/', views.keepermarkeredit_add),
    url(r'^keepermarkeredit_delete/(?P<marker_id>\d+)/', views.keepermarkeredit_delete),
    url(r'^keepermarkereedit/(?P<marker_id>\d+)/', views.keepermarkereedit),
    url(r'^keepermarker/', views.keepermarker),
    url(r'^newkeeper/', views.newkeeperform),
    url(r'^addkeeper/', views.addkeeper),
    url(r'^editkeeper/(?P<keeper_id>\d+)/', views.editkeeperform),
    url(r'^theeditkeeper/(?P<keeper_id>\d+)/', views.editkeeper),
    url(r'^deletekeeper/(?P<keeper_id>\d+)/', views.deletekeeper),
    url(r'^keeper/all/$', views.keepers),
    url(r'^keeper/get/(?P<keeper_id>\d+)/(?P<page_number>\d+)/', views.keeper),
    url(r'^keeper/get/(?P<keeper_id>\d+)/', views.keeper),
    url(r'^keeper/addfeedback/(?P<keeper_id>\d+)/$', views.addfeedback),
    url(r'^keepers_clean_search/', views.keepers_clean_search),
    url(r'^page/(\d+)/$', views.keepers),
    url(r'^page/(\d+)/(?P<searchlabe>\w+)/', views.keepers),
    url(r'error/(?P<error_text>\w+)/', views.Error),
    url(r'^$', views.keepers),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)