from django.urls import path
from . import views

# 设置命名空间
app_name = 'cms'

# 新闻管理url
urlpatterns = [
    path('', views.index, name='index'),
    path('write_news/', views.WriteNewsView.as_view(), name='write_news'),
    path('edit_news/', views.EditNewsView.as_view(), name='edit_news'),
    path('delete_news/', views.delete_news, name='delete_news'),
    path('news_category/', views.news_category, name='news_category'),
    path('add_news_category/', views.add_news_category, name='add_news_category'),
    path('edit_news_category/', views.edit_news_category, name='edit_news_category'),
    path('delete_news_category/', views.delete_news_category, name='delete_news_category'),
    path('banners/', views.banners, name='banners'),
    path('add_banner/', views.add_banner, name='add_banner'),
    path('banner_list/', views.banner_list, name='banner_list'),
    path('delete_banner/', views.delete_banner, name='delete_banner'),
    path('edit_banner/', views.edit_banner, name='edit_banner'),
    path('news_list/', views.NewsListView.as_view(), name='news_list'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('qntoken/', views.qntoken, name='qntoken'),
]

from . import course_views

# 课程管理url
urlpatterns += [
    path('pub_course/', course_views.PubCourseView.as_view(), name='pub_course'),
    path('course_category/', course_views.course_category, name='course_category'),
    path('add_course_category/', course_views.add_course_category, name='add_course_category'),
    path('edit_course_category/', course_views.edit_course_category, name='edit_course_category'),
    path('delete_course_category/', course_views.delete_course_category, name='delete_course_category'),
]
