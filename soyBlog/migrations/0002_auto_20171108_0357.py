# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-08 03:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('soyBlog', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TagPost',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='user_id',
            new_name='child_position',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='position',
            new_name='login_id',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post_id',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author_id',
        ),
        migrations.RemoveField(
            model_name='post',
            name='category_id',
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='soyBlog.Post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replied_comments', to='soyBlog.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='soyBlog.User'),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_posts', to='soyBlog.User'),
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category_posts', to='soyBlog.Category'),
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(related_name='tag_posts', to='soyBlog.Tag'),
        ),
    ]