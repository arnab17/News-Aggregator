from django.db import models
from datetime import datetime    

# Create your models here.


class News(models.Model):
	news_url = models.CharField(max_length=500)
	news_title = models.CharField(max_length=500)
	news_body = models.CharField(max_length=500)
	news_category = models.CharField(max_length=500, default='SOME_STRING')
	news_date = models.DateTimeField(default=datetime.now)
	news_rsslink = models.CharField(max_length=500, default='SOME_STRING')
	news_rank = models.IntegerField(default=0)
	news_img_url = models.CharField(max_length=500, default = 'SOME_STRING')
	news_country_id = models.IntegerField(default=0)	

	def __str__(self):
		return self.news_title	

	class Meta:
		ordering = ['-news_date']
class Country(models.Model):
	country_id = models.IntegerField(default=0)
	country_name = models.CharField(max_length=500, default = 'SOME_STRING')

	def __str__(self):
		return self.country_name

class Category(models.Model):
	category_id = models.CharField(max_length=500)
	category_name = models.CharField(max_length=500)	
	
	def __str__(self):
		return self.category_name

class Rsslinks1(models.Model):
	rss_link = models.CharField(max_length=500)
	link_rank = models.IntegerField(default=0)
	country_id = models.IntegerField(default=0)
	

class Rsslinks2(models.Model):
    rss_link = models.CharField(max_length=500)
    link_rank = models.IntegerField(default=0)
    country_id = models.IntegerField(default=0)

class Rsslinks3(models.Model):
        rss_link = models.CharField(max_length=500)
        link_rank = models.IntegerField(default=0)
        country_id = models.IntegerField(default=0)


class Rsslinks4(models.Model):
        rss_link = models.CharField(max_length=500)
        link_rank = models.IntegerField(default=0)
        country_id = models.IntegerField(default=0)


class Rsslinks5(models.Model):
        rss_link = models.CharField(max_length=500)
        link_rank = models.IntegerField(default=0)
        country_id = models.IntegerField(default=0)

