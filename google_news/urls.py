from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
	url(r'^$',views.get_top_stories,name='top_stories'),
	#url(r'^US/$',views.get_top_stories_us,name='us'),
	url(r'^Sports/$',views.get_sports,name='sports'),
        #url(r'^Sports/US/$',views.get_sports_us,name='sports_us'),
	url(r'^Entertainment/$',views.get_entertainment,name='entertainment'),
        #url(r'^Entertainment/US/$',views.get_entertainment_us,name='entertainment_us'),
	url(r'^Technology/$',views.get_technology,name='technology'),	
        #url(r'^Technology/US/$',views.get_technology_us,name='technology_us'),
	url(r'^Business/$',views.get_business,name='business'),
        #url(r'^Business/US/$',views.get_business_us,name='business_us'),
	url(r'^Science/$',views.get_science,name='science'),
        #url(r'^Science/US/$',views.get_science_us,name='science_us'),
	url(r'^World/$',views.get_world,name='world'),
        #url(r'^World/US/$',views.get_world_us,name='world_us'),
	url(r'^fetch/$',views.fetching_news,name='fetch'),
        url(r'^search/$',views.search_news,name='search'),
        path('showkeywordnews/<str:key>/',views.open_keyword_page,name='open_keyword_page'),
	path('fetchlocation/<int:country>/',views.change_location,name='fetch_location'),
]
