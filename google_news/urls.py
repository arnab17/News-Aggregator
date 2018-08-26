from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.get_top_stories,name='top_stories'),
	url(r'^Sports/$',views.get_sports,name='sports'),
	url(r'^Entertainment/$',views.get_entertainment,name='entertainment'),
	url(r'^Technology/$',views.get_technology,name='technology'),	
	url(r'^Business/$',views.get_business,name='business'),
	url(r'^Science/$',views.get_science,name='science'),
	url(r'^World/$',views.get_world,name='world'),
	url(r'^fetch/$',views.fetching_news,name='fetch'),
]
