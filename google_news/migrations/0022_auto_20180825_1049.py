# Generated by Django 2.1 on 2018-08-25 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_news', '0021_rsslinks6_rsslinks7'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='news_url',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]