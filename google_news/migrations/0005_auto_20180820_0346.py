# Generated by Django 2.1 on 2018-08-20 03:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_news', '0004_news_news_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['news_date']},
        ),
        migrations.AlterField(
            model_name='news',
            name='news_date',
            field=models.DateTimeField(default=datetime.datetime.now, editable=False),
        ),
    ]