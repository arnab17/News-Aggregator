# Generated by Django 2.1 on 2018-08-28 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('google_news', '0026_auto_20180827_1931'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cluster',
            unique_together={('cluster_id', 'cluster_category_id', 'cluster_country_id')},
        ),
    ]