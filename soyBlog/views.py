# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.safestring import mark_safe
from math import ceil
from mistune import markdown
from collections import defaultdict
from .models import Post

def safe_markdown(md_string):
    return mark_safe(markdown(md_string))

def home(request, page=''):
    context = {}

    context['page_info'] = {}
    context['page_info']['title'] = 'Home'
    context['page_info']['toggle'] = 'blog_home'

    post_perpage = 3.0
    page_count = Post.objects.count()
    max_page = ceil(page_count/post_perpage)
    page = page = min(int(page) if page.isdigit() and int(page) > 0 else 1, max_page)

    context['posts'] = Post.objects.order_by('-id')[(page - 1) * post_perpage : page * post_perpage]
    for post in context['posts']:
        post.content = safe_markdown(post.content)
    context['next_page'] = page + 1 if page < max_page else None
    context['prev_page'] = page - 1 if page > 1 else None

    return render(request, 'soyBlog/main.html', context)

def post(request, post_id):
    context = {}

    context['page_info'] = {}
    context['page_info']['toggle'] = 'blog_home'

    cur_post = Post.objects.get(id=post_id)
    prev_posts = Post.objects.filter(id__lt=post_id).order_by('-id')[:1] or None
    next_posts = Post.objects.filter(id__gt=post_id).order_by('id')[:1] or None

    cur_post.content = safe_markdown(cur_post.content)

    context['post'] = cur_post
    context['page_info']['title'] = cur_post.title
    context['prev_post'] = prev_posts[0] if prev_posts else None
    context['next_post'] = next_posts[0] if next_posts else None

    return render(request, 'soyBlog/post.html', context)

def archives(request):
    context = {}

    context['page_info'] = {}
    context['page_info']['title'] = 'Archives'
    context['page_info']['toggle'] = 'blog_archives'

    posts = Post.objects.order_by('-id')

    posts_by_year = defaultdict(list)
    for post in posts:
        posts_by_year[post.create_time.year].append(post)
    context['posts_year'] = sorted(posts_by_year.items(), reverse = True)

    return render(request, 'soyBlog/archives.html', context)

def getAllCategory(request, post_id):
    context = {}

    context['page_info'] = {}
    context['page_info']['title'] = 'soy'
    context['page_info']['toggle'] = 'blog_home'

    cur_post = Post.objects.get(id=post_id)
    prev_post = Post.objects.filter(id__lt=post_id).order_by('-id')[:1] or None
    next_post = Post.objects.filter(id__gt=post_id).order_by('id')[:1] or None

    cur_post.content = safe_markdown(cur_post.content)

    context['post'] = cur_post
    context['page_info']['title'] = cur_post.title
    context['prev_post'] = prev_post
    context['next_post'] = next_post

    return render(request, 'soyBlog/post.html', context)
