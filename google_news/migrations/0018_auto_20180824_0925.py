# Generated by Django 2.1 on 2018-08-24 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_news', '0017_auto_20180823_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='news_org_name',
            field=models.CharField(default='news_org', max_length=500),
        ),
        migrations.AddField(
            model_name='rsslinks1',
            name='org_name',
            field=models.CharField(default='news_org', max_length=500),
        ),
        migrations.AddField(
            model_name='rsslinks2',
            name='org_name',
            field=models.CharField(default='news_org', max_length=500),
        ),
        migrations.AddField(
            model_name='rsslinks3',
            name='org_name',
            field=models.CharField(default='news_org', max_length=500),
        ),
        migrations.AddField(
            model_name='rsslinks4',
            name='org_name',
            field=models.CharField(default='news_org', max_length=500),
        ),
        migrations.AddField(
            model_name='rsslinks5',
            name='org_name',
            field=models.CharField(default='news_org', max_length=500),
        ),
    ]