"""gongjiao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app.views import *

urlpatterns = [
    url(r'^manager/', include(admin.site.urls)),

    url(r'^api/user/add', user_add),
    url(r'^api/user/del', user_del),
    url(r'^api/user/edit', user_edit),
    url(r'^api/user/list', user_list),

    url(r'^api/place/add', place_add),
    url(r'^api/place/del', place_del),
    url(r'^api/place/edit', place_edit),
    url(r'^api/place/list$', place_list),
    url(r'^api/place/del_route', place_del_route),
    url(r'^api/place/listbyroute', place_list_byroute),


    url(r'^api/route/add', route_add),
    url(r'^api/route/del', route_del),
    url(r'^api/route/edit', route_edit),
    url(r'^api/route/list$', route_list),
    url(r'^api/route/listbyroute', route_search),

    url(r'^api/echart/gjw', echart_gjw),
    url(r'^api/echart/zzt', echart_zzt),
    url(r'^api/echart/bzt', echart_bzt),

    url(r'^api/cx', cx),

    url(r'^api/login', login),
    url(r'^api/logout', logout),
    url(r'^api/register', register),
]
