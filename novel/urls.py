"""定义novel的URL模式"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'novel_content/(?P<novelid>\d+)/$', views.detail, name='novel_content'),
    url(r'chapter/(?P<chapterid>\d+)/$', views.chapter, name='chapter'),
    url(r'sort_list/(?P<type>\d+)/(?P<page>\d+)/$', views.more, name='sort_list'),
    url(r'search/$', views.search, name='search')
]