import time
import string
import feedparser
import nltk
import re
import math
import gensim
import pattern
import requests
import difflib
import operator
import html.parser
from bs4 import BeautifulSoup
from sklearn.cluster import KMeans
from datetime import timedelta
from gensim.utils import lemmatize
from geolite2 import geolite2
from time import mktime
from datetime import datetime, timezone
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from newspaper import Article
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import fcluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist


from django.db.models import F
from .models import News
from .models import Country
from .models import Category 
from .models import Cluster 
from .models import Keyword
from .models import Rsslinks1
from .models import Rsslinks2
from .models import Rsslinks3
from .models import Rsslinks4
from .models import Rsslinks5
from .models import Rsslinks6
from .models import Rsslinks7
from .models import Location 
from .models import Cached_Keyword
from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

cachedStopWords = stopwords.words("english")

def remove_stop_words(stripped):
	return ' '.join([word for word in stripped if word not in cachedStopWords])

def posNN(text):
    tokens = []
    for word in lemmatize(text):
        st = word.decode("utf-8").split("/")
        if st[1] == 'NN' or st[1] == 'VB':
            tokens.append(st[0])
    stop = open("stop.txt", "r").read().split("\n")
    filtered_tokens = [token for token in tokens if token not in stop]
    return " ".join(filtered_tokens) 

def clean_article(article_unclean_text):
	article_unclean_text = article_unclean_text.replace("\n"," ")
	article_words = article_unclean_text.split()
	article_words = [word.lower() for word in article_words]
	table = str.maketrans('', '', string.punctuation)
	stripped = [word.translate(table) for word in article_words]
	article_clean_text = remove_stop_words(stripped)
	return article_clean_text


# categories :
# 
# 1. Politics
# 2. Sports
# 3. Entertainment
# 4. Technology
# 5. Business

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    stemmer = SnowballStemmer("english")
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def url_exists(news_url):
	exist_count = News.objects.filter(news_url = news_url).count()

	if exist_count >= 1:
		return True
	else:
		return False


def delete_news_rss():
	rss_link = 'http://feeds.foxnews.com/foxnews/most-popular'

	News.objects.filter(news_rsslink = rss_link).delete()

def fetching_news(request):
	num_category = 7
	start_clustering()
	Cached_Keyword.objects.all().delete()
	get_in_the_news_keywords(1)
	get_in_the_news_keywords(2)
	return HttpResponse("data loading done")

"""
	rss_links = Rsslinks1.objects.all()
	print("Getting the news for Category 1")
	for links in rss_links:
		news_rss = links.rss_link
		news_country = links.country_id
		news_org = links.org_name
		d = feedparser.parse(news_rss.strip())
		new_news = 0
		print(news_rss.strip())
		cnt_post = 0
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				new_news = new_news + 1

			if(cnt_post > 30):
				break

		news_update = News.objects.filter(news_rsslink = news_rss.strip()).update(news_rank = F('news_rank') + new_news)
		
		news_rank = 1
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			now = datetime.now()
			if url_exists(post.link):
				break
			else:
				try:
					print(post.title)
					print(post.link)
					response = requests.get(post.link)
					soup = BeautifulSoup(response.text)
					metas = soup.find_all('meta')
					keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'news_keywords' ]					
					print(keywords)
					if len(keywords) == 0:
						keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'keywords' ]
					if len(keywords) == 0:
						print(news_org, "***********************it does not have keywords ****************************")
					for keys in keywords:
							for key in re.findall(r"[\w\s]+",keys):
								key = key.strip()
								if key == '' or key == ' ' or len(key) == 1:
									continue
								Keyword.objects.create(keyword_name = key.lower(), news_url = post.link)
					article = Article(post.link)
					article.download()
					article.parse()
					print(article.summary)
					article_body = posNN(str(article.text))
					news_summary = str(article.text)
					news_summary = news_summary.replace("\n"," ")
					title = post.title
					html_parser = html.parser.HTMLParser()
					unescaped = html_parser.unescape(title) 
					news_instance = News.objects.create(news_url = post.link, news_title = unescaped, news_body = article_body, news_category = "1", news_date = datetime.now(timezone.utc), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org, news_summary = news_summary[:300] + "...")
					news_rank = news_rank + 1
				except Exception as e:
					print(e)

			if(cnt_post > 30):
				break

	
	rss_links = Rsslinks2.objects.all()
	print("Getting the news for Category 2")
	for links in rss_links:
		news_rss = links.rss_link 
		news_country = links.country_id
		news_org = links.org_name
		d = feedparser.parse(news_rss.strip())
		new_news = 0
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				new_news = new_news + 1
			if(cnt_post > 30):
				 break

		news_update = News.objects.filter(news_rsslink = news_rss.strip()).update(news_rank = F('news_rank') + new_news)
		
		news_rank = 1
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				try:
					print(post.title)
					print(post.link)
					response = requests.get(post.link)
					soup = BeautifulSoup(response.text)
					metas = soup.find_all('meta')
					keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'news_keywords' ]					
					print(keywords)
					if len(keywords) == 0:
						keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'keywords' ]
					if len(keywords) == 0:
						print(news_org, "***********************it does not have keywords ****************************")
					for keys in keywords:
							for key in re.findall(r"[\w\s]+",keys):
								key = key.strip()
								if key == '' or key == ' ' or len(key) == 1:
									continue
								Keyword.objects.create(keyword_name = key.lower(), news_url = post.link)
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_summary = str(article.text)
					news_summary = news_summary.replace("\n"," ")
					title = post.title
					html_parser = html.parser.HTMLParser()
					unescaped = html_parser.unescape(title) 
					news_instance = News.objects.create(news_url = post.link, news_title = unescaped, news_body = article_body, news_category = "2", news_date = datetime.now(timezone.utc), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org, news_summary = news_summary[:300] + "...")
					news_rank = news_rank + 1
				except Exception as e:
					print(e)	
			if(cnt_post > 30):
				break				

	
	rss_links = Rsslinks3.objects.all()
	print("Getting the news for Category 3")
	for links in rss_links:
		news_rss = links.rss_link 
		news_country = links.country_id
		news_org = links.org_name
		d = feedparser.parse(news_rss.strip())
		new_news = 0
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				new_news = new_news + 1
			if(cnt_post > 30):
				break

		news_update = News.objects.filter(news_rsslink = news_rss.strip()).update(news_rank = F('news_rank') + new_news)
		
		news_rank = 1
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				try:
					print(post.title)
					print(post.link)
					response = requests.get(post.link)
					soup = BeautifulSoup(response.text)
					metas = soup.find_all('meta')
					keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'news_keywords' ]					
					print(keywords)
					if len(keywords) == 0:
						keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'keywords' ]
					if len(keywords) == 0:
						print(news_org, "***********************it does not have keywords ****************************")
					for keys in keywords:
							for key in re.findall(r"[\w\s]+",keys):
								key = key.strip()
								if key == '' or key == ' ' or len(key) == 1:
									continue
								Keyword.objects.create(keyword_name = key.lower(), news_url = post.link)
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_summary = str(article.text)
					news_summary = news_summary.replace("\n"," ")
					title = post.title
					html_parser = html.parser.HTMLParser()
					unescaped = html_parser.unescape(title) 
					news_instance = News.objects.create(news_url = post.link, news_title = unescaped, news_body = article_body, news_category = "3", news_date = datetime.now(timezone.utc), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org, news_summary = news_summary[:300]+ "...")
					news_rank = news_rank + 1
				except Exception as e:
					print(e)
			if(cnt_post > 30):
				break
	

	rss_links = Rsslinks4.objects.all()
	print("Getting the news for Category 4")
	for links in rss_links:
		news_rss = links.rss_link 
		news_country = links.country_id
		news_org = links.org_name
		d = feedparser.parse(news_rss.strip())
		new_news = 0
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				new_news = new_news + 1
			if(cnt_post > 30):
				break

		news_update = News.objects.filter(news_rsslink = news_rss.strip()).update(news_rank = F('news_rank') + new_news)
		
		news_rank = 1
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post+1
			if url_exists(post.link):
				break
			else:
				try:
					print(post.title)
					print(post.link)
					response = requests.get(post.link)
					soup = BeautifulSoup(response.text)
					metas = soup.find_all('meta')
					keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'news_keywords' ]					
					print(keywords)
					if len(keywords) == 0:
						keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'keywords' ]
					if len(keywords) == 0:
						print(news_org, "***********************it does not have keywords ****************************")
					for keys in keywords:
							for key in re.findall(r"[\w\s]+",keys):
								key = key.strip()
								if key == '' or key == ' ' or len(key) == 1:
									continue
								Keyword.objects.create(keyword_name = key.lower(), news_url = post.link)
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_summary = str(article.text)
					news_summary = news_summary.replace("\n"," ")
					title = post.title
					html_parser = html.parser.HTMLParser()
					unescaped = html_parser.unescape(title) 
					news_instance = News.objects.create(news_url = post.link, news_title = unescaped, news_body = article_body, news_category = "4", news_date = datetime.now(timezone.utc), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org, news_summary = news_summary[:300]+ "...")
					news_rank = news_rank + 1
				except Exception as e:
					print(e)
			if(cnt_post > 30):
				break


	rss_links = Rsslinks5.objects.all()
	print("Getting the news for Category 5")
	for links in rss_links:
		news_rss = links.rss_link 
		news_country = links.country_id
		news_org = links.org_name
		d = feedparser.parse(news_rss.strip())
		new_news = 0
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				new_news = new_news + 1
			if(cnt_post > 30):
				break

		news_update = News.objects.filter(news_rsslink = news_rss.strip()).update(news_rank = F('news_rank') + new_news)
		
		news_rank = 1
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				try:
					print(post.title)
					print(post.link)
					response = requests.get(post.link)
					soup = BeautifulSoup(response.text)
					metas = soup.find_all('meta')
					keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'news_keywords' ]					
					print(keywords)
					if len(keywords) == 0:
						keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'keywords' ]
					if len(keywords) == 0:
						print(news_org, "***********************it does not have keywords ****************************")
					for keys in keywords:
							for key in re.findall(r"[\w\s]+",keys):
								key = key.strip()
								if key == '' or key == ' ' or len(key) == 1:
									continue
								Keyword.objects.create(keyword_name = key.lower(), news_url = post.link)
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_summary = str(article.text)
					news_summary = news_summary.replace("\n"," ")
					title = post.title
					html_parser = html.parser.HTMLParser()
					unescaped = html_parser.unescape(title) 
					news_instance = News.objects.create(news_url = post.link, news_title = unescaped, news_body = article_body, news_category = "5", news_date = datetime.now(timezone.utc), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org, news_summary = news_summary[:300]+ "...")
					news_rank = news_rank + 1
				except Exception as e:
					print(e)
			if(cnt_post > 30):
				break

	rss_links = Rsslinks6.objects.all()
	print("Getting the news for Category 6")
	for links in rss_links:
		news_rss = links.rss_link 
		news_country = links.country_id
		news_org = links.org_name
		d = feedparser.parse(news_rss.strip())
		new_news = 0
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				new_news = new_news + 1
			if(cnt_post > 30):
				break

		news_update = News.objects.filter(news_rsslink = news_rss.strip()).update(news_rank = F('news_rank') + new_news)
		
		news_rank = 1
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				try:
					print(post.title)
					print(post.link)
					response = requests.get(post.link)
					soup = BeautifulSoup(response.text)
					metas = soup.find_all('meta')
					keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'news_keywords' ]					
					print(keywords)
					if len(keywords) == 0:
						keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'keywords' ]
					if len(keywords) == 0:
						print(news_org, "***********************it does not have keywords ****************************")
					for keys in keywords:
							for key in re.findall(r"[\w\s]+",keys):
								key = key.strip()
								if key == '' or key == ' ' or len(key) == 1:
									continue
								Keyword.objects.create(keyword_name = key.lower(), news_url = post.link)
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_summary = str(article.text)
					news_summary = news_summary.replace("\n"," ")
					title = post.title
					html_parser = html.parser.HTMLParser()
					unescaped = html_parser.unescape(title) 
					news_instance = News.objects.create(news_url = post.link, news_title = unescaped, news_body = article_body, news_category = "6", news_date = datetime.now(timezone.utc), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org, news_summary = news_summary[:300]+ "...")
					news_rank = news_rank + 1
				except Exception as e:
					print(e)
			if(cnt_post > 30):
				break


	rss_links = Rsslinks7.objects.all()
	print("Getting the news for Category 7")
	for links in rss_links:
		news_rss = links.rss_link 
		news_country = links.country_id
		news_org = links.org_name
		d = feedparser.parse(news_rss.strip())
		new_news = 0
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				new_news = new_news + 1
			if(cnt_post > 30):
				break

		news_update = News.objects.filter(news_rsslink = news_rss.strip()).update(news_rank = F('news_rank') + new_news)
		
		news_rank = 1
		cnt_post = 0
		print(news_rss.strip())
		for post in d.entries:
			cnt_post = cnt_post + 1
			if url_exists(post.link):
				break
			else:
				try:
					print(post.title)
					print(post.link)
					response = requests.get(post.link)
					soup = BeautifulSoup(response.text)
					metas = soup.find_all('meta')
					keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'news_keywords' ]					
					print(keywords)
					if len(keywords) == 0:
						keywords = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'keywords' ]
					if len(keywords) == 0:
						print(news_org, "***********************it does not have keywords ****************************")
					for keys in keywords:
							for key in re.findall(r"[\w\s]+",keys):
								key = key.strip()
								if key == '' or key == ' ' or len(key) == 1:
									continue
								Keyword.objects.create(keyword_name = key.lower(), news_url = post.link)
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_summary = str(article.text)
					news_summary = news_summary.replace("\n"," ")
					title = post.title
					html_parser = html.parser.HTMLParser()
					unescaped = html_parser.unescape(title) 
					news_instance = News.objects.create(news_url = post.link, news_title = unescaped, news_body = article_body, news_category = "7", news_date = datetime.now(timezone.utc), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org, news_summary = news_summary[:300]+ "...")
					news_rank = news_rank + 1
				except Exception as e:
					print(e)
			if(cnt_post > 30):
				break
	
	start_clustering()
	Cached_Keyword.objects.all().delete()
	get_in_the_news_keywords(1)
	get_in_the_news_keywords(2)
	return HttpResponse("data loading done")
"""

#tfidf_vectorizer = TfidfVectorizer(use_idf=True, ngram_range=(1,3))
#tfidf_matrix = tfidf_vectorizer.fit_transform(content_as_str) #fit the vectorizer to synopses

def get_similarity_matrix(content_as_str, global_cleaned_content_as_str):
	tfidf_vectorizer = TfidfVectorizer(use_idf=True, ngram_range=(1,3))
	tfidftemp = tfidf_vectorizer.fit(global_cleaned_content_as_str)
	tfidf_matrix = tfidf_vectorizer.transform(content_as_str)
	similarity_matrix = cosine_similarity(tfidf_matrix)
	return (similarity_matrix, tfidf_matrix)

"""
def get_top_stories_us(request):
	return show_news(request,1,2)
def get_sports_us(request):
	return show_news(request,2,2)
def get_entertainment_us(request):
	return show_news(request,3,2)
def get_technology_us(request):
	return show_news(request,4,2)
def get_business_us(request):
	return show_news(request,5,2)
def get_science_us(request):
	return show_news(request,6,2)
def get_world_us(request):
	return show_news(request,7,2)
"""

def get_top_stories(request):
	return show_news(request, 1)

def get_sports(request):
	return show_news(request, 2)
	
def get_entertainment(request):
	return show_news(request, 3)

def get_technology(request):
	return show_news(request, 4)

def get_business(request):
	return show_news(request, 5)

def get_science(request):
	return show_news(request,6)

def get_world(request):
	return show_news(request,7)	


def correct_keywords():
	print("***********fetch")
	for keys in Keyword.objects.all():
		print(keys.keyword_name)
		for key in re.findall(r"[\w\s]+",keys.keyword_name):
			key = key.strip()
			if key == '' or key == ' ' or len(key) == 1:
				continue
			Keyword.objects.create(keyword_name = key.lower(), news_url = keys.news_url)
	print("***************************end")	

def get_loc_from_ip(client_ip):
	#client_ip = get_client_ip(request)
	reader = geolite2.reader()
	print(client_ip)
	if client_ip == '127.0.0.1' :
		client_ip = '1.7.255.255'
	print(client_ip)
	d = reader.get(client_ip)
	print("-----")
	print(d)
	print("-----")
	country_name = "India"
	#country_name = d['country']['names']['en']
	return country_name
	
def get_location(client_ip):
	try :
		location_instance = Location.objects.get(ip_address = client_ip)
		return location_instance.location_id
	except:
		print("New User")
		country_name = get_loc_from_ip(client_ip)
		country_instance = Country.objects.get(country_name = country_name)
		Location.objects.create(ip_address = client_ip, location_id = country_instance.country_id)
		return country_instance.country_id	

def change_location(request, country):
	print("Changing location to - ", country)
	client_ip = get_client_ip(request)
	#Location.objects.all().delete()
	Location.objects.filter(ip_address = client_ip).update(location_id = country)
	#Location.objects.create(location_id = country)
	return redirect('/google_news/')

def show_news(request, category):
	#client_ip = get_client_ip(request)
	#reader = geolite2.reader()
	#print(client_ip)
	#client_ip = '1.7.255.255'
	#print(client_ip)
	#d = reader.get(client_ip)
	#country_name = d['country']['names']['en']
	#print(country_name)

	#country_instance = Country.objects.get(country_name = country_name)

	#print(country_instance.country_id)

	#correct_keywords()

	category_instance = Category.objects.get(category_id = category)

	country_id = get_location(get_client_ip(request))

	list_of_cluster = fetch_all_clusters(category, country_id)
	list_of_keyword = show_keywords(country_id)
	if len(list_of_keyword) == 0:
		list_of_keyword = get_in_the_news_keywords(country_id)
	#print(list_of_keyword, "*********list of kw************")
	#k = Keyword.objects.filter(keyword_name = '')
	#print(k)
	#k =  Keyword.objects.filter(keyword_name = ' ')
	#print(k)


	return render(request, 'google_news/post_list.html', {'list_of_cluster':list_of_cluster, 'category':category_instance.category_name, 'list_of_keyword':list_of_keyword})

def show_keywords(country_id):
	return [key.keyword_name for key in Cached_Keyword.objects.filter(keyword_country_id=country_id)]

def search_news(request):
	if request.method == 'GET':
		search_query = request.GET.get('search', None)

		country_id = get_location(get_client_ip(request))

		list_of_cluster = []
		list_of_keyword = show_keywords(country_id)
		keywords = {}
		category_name = search_query
		
		keyword_mapping = {}

		tags = search_query.split()
		len_of_query = len(tags)
		print("Stripped Tags : ")
		print(tags)
		for k in Keyword.objects.all():
			k_name = k.keyword_name.lower().split()
			for name in k_name:
				if name not in  keywords:
					keywords[name] = []
				if k.news_url not in keywords[name]:
					keywords[name].append(k.news_url)
		keys = []
		for key in tags:
			key = key.lower()
			gen_keys = difflib.get_close_matches(key, [k for k in keywords.keys()], cutoff = 0.7)
			for new_keys in gen_keys :
				if new_keys not in keyword_mapping :
					keyword_mapping[new_keys] = []
				keyword_mapping[new_keys] = key
				# In the keyword mapping dictionary we create a mapping of the derived word to the root word  
			keys += difflib.get_close_matches(key, [k for k in keywords.keys()], cutoff = 0.7)
		matching_news = {}
		url_keyword_votes = {}
		print(keys)
		for key in keys:
			root_key = keyword_mapping[key]
			for article_url in keywords[key]:
				if article_url not in url_keyword_votes :
					url_keyword_votes[article_url] = []
				if root_key in url_keyword_votes[article_url] :
					continue
				else :
					if article_url not in matching_news:
						matching_news[article_url] = 0
					url_keyword_votes[article_url].append(root_key)
					matching_news[article_url] += 1
		
		#sorted_list_of_news = sorted(matching_news, key=matching_news.get, reverse=True)

		max_val = 0

		for key,value in matching_news.items() :
			max_val = max(max_val, value)

		new_news = {}

		for key,value in matching_news.items() :
			if value == 1 :
				if max_val > value :
					if len_of_query == 1 :
						new_news[key] = value
					else :
						continue
				else :
					new_news[key] = value
			else :
				new_news[key] = value

		sorted_list_of_news = sorted(new_news, key=matching_news.get, reverse=True)

		list_of_cluster = []
		for article_url in sorted_list_of_news:
			try:
				news = News.objects.get(news_url = article_url)
				tlen = len(tags)
				tmp = 0
				for key in tags :
					key = key.lower()
					print(key)
					print(news.news_url)
					if key in news.news_body :
						tmp = tmp + 1

				val = tmp / tlen

				print(val)
				#if val > 0.5 :
				cluster = [(news.news_url, news.news_title, news.news_img_url, get_time(news.news_date), news.news_rank,news.news_org_name,news.news_summary)]
				list_of_cluster.append(cluster)
			except:
				print("Some error occured")

		return render(request, 'google_news/post_list.html', {'list_of_cluster':list_of_cluster, 'category':category_name, 'list_of_keyword':list_of_keyword})
	

def open_keyword_page(request,key):
	country_id = get_location(get_client_ip(request))
	list_of_cluster = []
	list_of_keyword = show_keywords(country_id)
	keywords = {}
	print("*********************start show keywords**********************************88")
	for k in Keyword.objects.all():
		k_name = k.keyword_name.lower();
		if k_name not in  keywords:
			keywords[k_name] = []
		keywords[k_name].append(k.news_url)
	keys = difflib.get_close_matches(key, [k for k in keywords.keys()], cutoff = 0.82)
	print(keys)
	category_name = key.upper()
	print(len(keywords), '**************************')
	visited = []
	print(len(News.objects.all()))
	for k in keys:
		for article_url in keywords[k]: 
			if article_url not in visited:
				visited.append(article_url)
				print(article_url)
				try:
					news = News.objects.get(news_url = article_url)
					print(news)
					cluster = [(news.news_url, news.news_title, news.news_img_url, get_time(news.news_date), news.news_rank,news.news_org_name,news.news_summary)]
					list_of_cluster.append(cluster)
				except:
					print("Gone wrong")
	return render(request, 'google_news/post_list.html', {'list_of_cluster':list_of_cluster, 'category':category_name, 'list_of_keyword':list_of_keyword})


def get_in_the_news_keywords(country_id):
	list_of_cluster = []
	for i in range(1, 8):
		list_of_cluster += fetch_all_clusters(i, country_id)[:3]
	final_list = []
	for cluster in list_of_cluster:
		temp_list = []
		for article in cluster:
			temp_list += fetch_keywords(article[0])
		temp_list = get_top_keywords(temp_list)
		for word in temp_list:
			if len(difflib.get_close_matches(word, final_list, cutoff = 0.7)) == 0:
				final_list.append(word)
	final_list = final_list[:22]
	for key in final_list:
		print(key)
		print("Entry into DB")
		Cached_Keyword.objects.create(keyword_name = key, keyword_country_id = country_id)	
	print("******************************")		
	return final_list

def fetch_keywords(news):
	return [keyword.keyword_name for keyword in Keyword.objects.filter(news_url = news)]

def get_top_keywords(temp_list):
	visited = []
	keywords = {}
	temp_list = [word.lower() for word in temp_list]
	for word in temp_list:
		if word == '' or word == ' ' or len(word) == 1:
			continue
		if len(difflib.get_close_matches(word, visited, cutoff = 0.7)) == 0:
			visited.append(word)
			keywords[word] = len(difflib.get_close_matches(word, temp_list, cutoff = 0.7))
	
	print(keywords)
	return sorted(keywords, key=keywords.get, reverse=True)[:1]

def fetch_all_clusters(category, country_id):
	clusters = Cluster.objects.filter(cluster_country_id = country_id, cluster_category_id = category)
	list_of_cluster = []
	for cluster in clusters:
		#print(cluster.cluster_id)
		list_of_cluster.append(fetch_cluster_news(cluster.cluster_id,country_id, category))

	return list_of_cluster

def get_time(date):
			now = datetime.now(timezone.utc)
			delta = now - date
			days, seconds = delta.days, delta.seconds

			if days > 0 :
				return str(days) + " days ago"
			else:
				hours = days*24 + seconds // 3600
				if hours > 5 :
					return "today"
				else:
					if hours > 0 :
						return str(hours) + " hours ago"
					else:
						minutes = ((seconds % 3600) // 60) + 1
						return str(minutes) + " minutes ago"


def fetch_cluster_news(cluster_id, cluster_country_id, cluster_category_id):
	news_list = []
	news_instance = News.objects.filter(news_cluster_id = cluster_id, news_country_id = cluster_country_id, news_category = str(cluster_category_id))
	for news in news_instance:
		news_list.append((news.news_url,news.news_title,news.news_img_url, get_time(news.news_date), news.news_rank,news.news_org_name,news.news_summary))
	return news_list

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def start_clustering():
	categories = 7
	num_countries = 2
	for x in range(num_countries):
		global_news_instance = News.objects.filter(news_country_id = x+1)
		for y in range(categories):
			news_instance = News.objects.filter(news_category=y+1, news_country_id = x+1)
			clusttering(news_instance,global_news_instance, x+1, y+1)


def sortrank(val):
	return int(val[4])

def sortbyscore(val):
	return val[0]

def get_rank(category, rss_link):
	print(rss_link)
	if category == 1 :
		rss_object = Rsslinks1.objects.get(rss_link = rss_link)
		return rss_object.link_rank
	if category == 2 :
		rss_object = Rsslinks2.objects.get(rss_link = rss_link)
		return rss_object.link_rank
	if category == 3 :
		rss_object = Rsslinks3.objects.get(rss_link = rss_link)
		return rss_object.link_rank
	if category == 4 :
		rss_object = Rsslinks4.objects.get(rss_link = rss_link)
		return rss_object.link_rank
	if category == 5 :
		rss_object = Rsslinks5.objects.get(rss_link = rss_link)
		return rss_object.link_rank
	if category == 6 :
		rss_object = Rsslinks6.objects.get(rss_link = rss_link)
		return rss_object.link_rank
	if category == 7 :
		rss_object = Rsslinks7.objects.get(rss_link = rss_link)
		return rss_object.link_rank

def clusttering(news_instance, global_news_instance, country_id, category):
	print(country_id)
	print(category)
	print("******************************Clustering Started***************************************")
	
	url_list = []
	cleaned_content_as_str = []
	global_cleaned_content_as_str = []
	published_date = []
	rss_link_list = []

	for article in global_news_instance:
		global_cleaned_content_as_str.append(article.news_body)

	for article in news_instance:
		url_list.append(article.news_url)
		cleaned_content_as_str.append(article.news_body)
		published_date.append(article.news_date)
		rss_link_list.append(article.news_rsslink)

	(similarity_matrix, tfidf_matrix) = get_similarity_matrix(cleaned_content_as_str,global_cleaned_content_as_str)
	dist = 1 - cosine_similarity(tfidf_matrix)
	
	Z = hierarchy.average(dist)

	c, coph_dists = cophenet(Z, pdist(dist))

	print(c)

	#print(url_list[48])
	#print(cleaned_content_as_str[48])

	#print()
	#print()

	#print(url_list[78])
	#print(cleaned_content_as_str[78])

	print(Z[:120])


	cluster_labels = fcluster(Z, 1.33, criterion='distance')
	d = {}
	iterator_index = 0

	Cluster.objects.filter(cluster_category_id = category, cluster_country_id = country_id).delete() 

	for x in cluster_labels:
		print(url_list[iterator_index])
		if x not in d:
			d[x] = []
			Cluster.objects.create(cluster_id = x, cluster_rank = 0, cluster_category_id = category, cluster_country_id = country_id)
		d[x].append((published_date[iterator_index], get_rank(category,rss_link_list[iterator_index])))
		#d[x].append((url_list[iterator_index],title_list[iterator_index], img_url[iterator_index], published_date[iterator_index], rank_list[iterator_index], org_name_list[iterator_index],get_rank(category,rss_link_list[iterator_index]),summary_list[iterator_index]))
		News.objects.filter(news_url = url_list[iterator_index]).update(news_cluster_id = x)
		iterator_index = iterator_index + 1

	cluster_scores = []

	for key in d:
		news_list = []
		score1 = 0
		score2 = 0
		tie_break_score  = 0
		org_dict = {}
		for date,org_rank in d[key]:
			if org_rank not in org_dict:
				org_dict[org_rank] = []
				score2 = score2 + 1
				if org_rank > 100 :
					tie_break_score = tie_break_score + 1
			org_dict[org_rank].append(org_rank)
			now = datetime.now(timezone.utc)
			delta = now - date
			days, seconds = delta.days, delta.seconds
			minutes = ((seconds % 3600) // 60) + 1

			if days > 0 :
				print("No score given")
			else:
				hours = days*24 + seconds // 3600
				tmp = 1 / (hours+1)
				score1 = score1 + tmp 				
		
		cluster_scores.append((score1*score2,key,float(tie_break_score)))

	#cluster_scores.sort(key = sortbyscore)	

	#sorted(cluster_scores, key=lambda x: (float(x[0]), float(x[2])))

	cluster_scores.sort(key = operator.itemgetter(0,2))

	rank_start = len(d)

	for x,y,z in cluster_scores:
		print("---------------")
		print(x)
		print(z)
		print(rank_start)
		print("---------------")
		Cluster.objects.filter(cluster_id = y, cluster_category_id = category, cluster_country_id = country_id).update(cluster_rank = rank_start)
		rank_start = rank_start - 1
