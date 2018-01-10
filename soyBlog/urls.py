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
from django.conf.urls import url
from django.contrib import admin
from soyBlog import views as soyBlog_views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', soyBlog_views.home, name='main'),
    url(r'^(?P<page>[0-9]+)$', soyBlog_views.home, name='main'),
    url(r'^post/(?P<post_id>[0-9]+)$', soyBlog_views.post, name='post'),
    url(r'^archives$', soyBlog_views.archives, name='archives'),
]
