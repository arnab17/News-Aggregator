from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.get_top_stories,name='top_stories'),
	url(r'^Sports/$',views.get_sports,name='sports'),
	url(r'^Trending/$',views.get_trending,name='trending'),
	url(r'^Technology/$',views.get_technology,name='technology'),	
	url(r'^Business/$',views.get_business,name='business'),
	url(r'^fetch/$',views.fetching_news,name='fetch'),
]
