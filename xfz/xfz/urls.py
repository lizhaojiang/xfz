"""xfz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from apps.news import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('cms/', include('apps.cms.urls')), #后台url
    path('search/', views.search, name='search'), #搜索页面单独url
    path('',views.index,name='index'), #首页单独url
    path('news/', include('apps.news.urls')), #有关新闻页面
    path('account/', include('apps.xfzauth.urls')), #有关用户权限(登录,退出)
    path('course/', include('apps.course.urls')),  # 创业课堂的url
    path('payinfo/', include('apps.payinfo.urls')),  # 支付的url
    path('ueditor/', include('apps.ueditor.urls')),  # 富文本编辑器
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path("__debug__/",include(debug_toolbar.urls)))