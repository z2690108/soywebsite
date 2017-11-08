# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

# 文章
class Post(models.Model):
  # 标题
  title = models.CharField(max_length=200, blank=False)
  # 内容
  content = models.TextField(blank=False)
  # 作者
  author = models.ForeignKey(User)
  # 分类
  category = models.ForeignKey(Category)
  # 标签
  tag = models.ForeignKey(Tag)
  # 创建时间
  creat_time = models.DateField(auto_now_add=True)
  # 修改时间
  modify_time = models.DateField(auto_now=True)

# 用户信息
class User(models.Model):
  # 用户id
  user_id = models.IntegerField(primary_key=True, blank=False)
  # 用户账号
  login_id = models.IntegerField(db_index=True, unique=True, blank=False) 
  # 用户名称
  name = models.IntegerField(blank=False)  
  # 用户邮箱
  email = models.EmailField() 
  # 介绍
  intro = models.TextField(max_length=2000)
  # 签名
  sign = models.TextField(max_length=200)
  # 创建时间
  creat_time = models.DateField(auto_now_add=True)
  # 修改时间
  modify_time = models.DateField(auto_now=True)

# 分类
class Category(models.Model):
  # 分类名
  name = models.CharField(max_length=200, blank=False)
  # 创建时间
  creat_time = models.DateField(auto_now_add=True)
  # 修改时间
  modify_time = models.DateField(auto_now=True)

# 标签
class Tag(models.Model):
  # 分类名
  name = models.CharField(max_length=200, blank=False)
  # 创建时间
  creat_time = models.DateField(auto_now_add=True)
  # 修改时间
  modify_time = models.DateField(auto_now=True)

# 评论表
class Comment(models.Model):
  # 文章
  post = models.ForeignKey(Post)
  # 评论楼层
  position = models.IntegerField(blank=False)
  # 子楼层
  child_position = models.IntegerField(blank=False)
  # 被回复id
  reply_user = models.ForeignKey(User)
  # 评论用户
  user = models.ForeignKey(User)
  # 内容
  content = models.TextField(max_length=2000, blank=False)
  # 创建时间
  creat_time = models.DateField(auto_now_add=True)
  # 修改时间
  modify_time = models.DateField(auto_now=True)





