# Generated by Django 3.2.9 on 2021-11-03 11:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogtype_blog_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogtype',
            name='blog_count',
        ),
    ]
