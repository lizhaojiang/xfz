from django.urls import path
from . import views

#设置命名空间
app_name = 'cms'

urlpatterns = [
    path('',views.index,name='index'),
    path('write_news/',views.WriteNewsView.as_view(),name='write_news'),
    path('news_category/', views.news_category, name='news_category'),
    path('add_news_category/', views.add_news_category, name='add_news_category'),
    path('edit_news_category/', views.edit_news_category, name='edit_news_category'),
    path('delete_news_category/', views.delete_news_category, name='delete_news_category'),
    path('banners/', views.banners, name='banners'),
    path('upload_file/', views.upload_file, name='upload_file'),
    path('qntoken/', views.qntoken, name='qntoken'),
]