import time
import string
import feedparser
import nltk
import re
import math
import gensim
import pattern
from sklearn.cluster import KMeans
from datetime import timedelta
from gensim.utils import lemmatize
from geolite2 import geolite2
from time import mktime
from datetime import datetime
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from newspaper import Article
from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import fcluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from django.db.models import F
from .models import News
from .models import Country
from .models import Category 
from .models import Rsslinks1
from .models import Rsslinks2
from .models import Rsslinks3
from .models import Rsslinks4
from .models import Rsslinks5
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
        #print(st)
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


def fetching_news(request):
	num_category = 5
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
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_instance = News.objects.create(news_url = post.link, news_title = post.title, news_body = article_body, news_category = "1", news_date = datetime.now(), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org)
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
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_instance = News.objects.create(news_url = post.link, news_title = post.title, news_body = article_body, news_category = "2", news_date = datetime.now(), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org)
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
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_instance = News.objects.create(news_url = post.link, news_title = post.title, news_body = article_body, news_category = "3", news_date = datetime.now(), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org)
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
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_instance = News.objects.create(news_url = post.link, news_title = post.title, news_body = article_body, news_category = "4", news_date = datetime.now(), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org)
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
					article = Article(post.link)
					article.download()
					article.parse()
					article_body = posNN(str(article.text))
					news_instance = News.objects.create(news_url = post.link, news_title = post.title, news_body = article_body, news_category = "5", news_date = datetime.now(), news_rsslink = news_rss.strip(), news_rank = news_rank, news_img_url = article.top_image, news_country_id = news_country, news_org_name = news_org)
					news_rank = news_rank + 1
				except Exception as e:
					print(e)
			if(cnt_post > 30):
				break
	return HttpResponse("data loading done")


#tfidf_vectorizer = TfidfVectorizer(use_idf=True, ngram_range=(1,3))
#tfidf_matrix = tfidf_vectorizer.fit_transform(content_as_str) #fit the vectorizer to synopses

def get_similarity_matrix(content_as_str, global_cleaned_content_as_str):
	tfidf_vectorizer = TfidfVectorizer(use_idf=True, ngram_range=(1,3))
	tfidftemp = tfidf_vectorizer.fit(global_cleaned_content_as_str)
	tfidf_matrix = tfidf_vectorizer.transform(content_as_str)
	similarity_matrix = cosine_similarity(tfidf_matrix)
	return (similarity_matrix, tfidf_matrix)

def get_top_stories(request):
	return show_news(request, 1)

def get_sports(request):
	return show_news(request, 2)
	
def get_trending(request):
	return show_news(request, 3)

def get_technology(request):
	return show_news(request, 4)

def get_business(request):
	return show_news(request, 5)
	

def get_cluster_kmeans(tfidf_matrix, num_clusters):
    km = KMeans(n_clusters = num_clusters)
    km.fit(tfidf_matrix)
    cluster_list = km.labels_.tolist()
    return cluster_list	

def show_news(request, category):
	client_ip = get_client_ip(request)
	reader = geolite2.reader()
	print(client_ip)
	client_ip = '1.7.255.255'
	d = reader.get(client_ip)
	country_name = d['country']['names']['en']
	print(country_name)

	country_instance = Country.objects.get(country_name = country_name)

	print(country_instance.country_id)

	category_instance = Category.objects.get(category_id = category)

	global_news_instance = News.objects.filter(news_country_id = country_instance.country_id)
	news_instance = News.objects.filter(news_category=category, news_country_id = country_instance.country_id)
	list_of_cluster = clusttering(news_instance,global_news_instance)
	return render(request, 'google_news/post_list.html', {'list_of_cluster':list_of_cluster, 'category':category_instance.category_name})
	

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def sortrank(val):
	return val[4]

def clusttering(news_instance, global_news_instance):
	url_list = []
	rank_list = []
	title_list = []
	cleaned_content_as_str = []
	global_cleaned_content_as_str = []
	img_url = []
	published_date = []
	org_name_list = []

	for article in global_news_instance:
		global_cleaned_content_as_str.append(article.news_body)

	for article in news_instance:
		org_name_list.append(article.news_org_name)
		rank_list.append(article.news_rank)
		url_list.append(article.news_url)
		title_list.append(article.news_title)
		cleaned_content_as_str.append(article.news_body)
		img_url.append(article.news_img_url)
		published_date.append(article.news_date)

	(similarity_matrix, tfidf_matrix) = get_similarity_matrix(cleaned_content_as_str,global_cleaned_content_as_str)
	dist = 1 - cosine_similarity(tfidf_matrix)
	Z = hierarchy.average(dist)


	print(Z)


	cluster_labels = fcluster(Z, 1.33, criterion='distance')
	d = {}
	iterator_index = 0
	for x in cluster_labels:
		if x not in d:
			d[x] = []
		d[x].append((url_list[iterator_index],title_list[iterator_index], img_url[iterator_index], published_date[iterator_index], rank_list[iterator_index], org_name_list[iterator_index]))
		iterator_index = iterator_index + 1
		
	list_of_clusters = []

	for key in d:
		news_list = []
			#response_string = response_string + "<h3>" + str(key) + "</h3> <br>"
		for urls,title,img,date,rank,org_name in d[key]:
			news_list.append((urls, title, img, date, rank, org_name))
				#response_string = response_string + "<h3>" + title + "</h3> <br> <a href=" + urls + ">Link</a> <br>"
		
		news_list.sort(key = sortrank)

		list_of_clusters.append(news_list)

	return list_of_clusters
