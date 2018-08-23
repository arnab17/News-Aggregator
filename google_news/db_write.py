import feedparser
import models
from .models import News
from .models import Category 
from newspaper import Article

num_category = 5
for x in range(num_category):
	filepath = 'categoryrss' + str(x) + '.txt'
	print(filepath)
	with open(filepath) as fp:
		line = fp.readline()
		cnt = 1
		print(cnt)
		while line:
			print("RSS LINK : " + line.strip())
			d = feedparser.parse(line.strip())
			print("here")
			for post in d.entries:
				print(post.title)
				print(post.link)
				if url_exists(post.link):
					print("News already exists")
				else:
					try:
						article = Article(post.link)
						article.download()
						article.parse()
						article_body = clean_article(str(article.text))
						news_instance = News.objects.create(news_url = post.link, news_title = post.title, news_body = article_body, news_category = str(x+1), news_date = datetime.fromtimestamp(mktime(post.published_parsed)))		
					except:
						print("Can't deal with it")		
			line = fp.readline()
			cnt += 1
