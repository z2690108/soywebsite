"""myset URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include, static
from django.contrib import admin
from myset import views as myset_views
from soyBlog import views as soyBlog_views
from steamCard import views as steamCard_views

import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$', myset_views.home, name='main'),
    url(r'^$', soyBlog_views.home, name='main'),
    url(r'^ms2mmlMaker/', include('ms2mmlMaker.urls', namespace='ms2mmlMaker')),
    url(r'^blog/', include('soyBlog.urls', namespace='soyBlog')),
    url(r'^steamCard/', include('steamCard.urls', namespace='steamCard')),    
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)