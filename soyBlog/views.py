# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from math import ceil
from .models import Post

def home(request, page=1):
  context = {}

  context['page_info'] = {}
  context['page_info']['title'] = 'soy'
  context['page_info']['toggle'] = 'blog_home'

  post_perpage = 3
  page_count = Post.objects.count()
  max_page = ceil(page_count/post_perpage)

  page = page if page > 0 else 1
  context['posts'] = Post.objects.all()[(page - 1) * post_perpage : post_perpage]
  context['next_page'] = page + 1 if page < max_page else None
  context['prev_page'] = page - 1 if page > 1 else None

  return render(request, 'soyBlog/main.html', context)
