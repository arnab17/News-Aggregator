# Generated by Django 2.1 on 2018-08-22 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google_news', '0012_news_news_rank'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='news_score',
        ),
    ]
