"""
Django settings for xfz project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=u$w69hw2qxdprc%3w3(ng&)f+@d)l%+q-w_z16iejl=+=h@1x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.xfzauth',
    'apps.cms',
    'apps.news',
    'apps.ueditor',
    'rest_framework',
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xfz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'front','templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            #设置static静态文件的路径,以后再模板中使用不需要再使用load
            'builtins':[
                'django.templatetags.static'
            ]
        },
    },
]

WSGI_APPLICATION = 'xfz.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "xfz",
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'USER': 'root',
        'PASSWORD': '123456'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#自定义user类,需要再系统中设置AUTH_USER_MODEL(app.模型),不设置django会使用默认的user
AUTH_USER_MODEL = 'xfzauth.User'


#配置缓冲,使用memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #配置可以访问的ip,多个IP使用列表
        'LOCATION': '127.0.0.1:11211'
    }
}



# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

#配置静态文件的路径
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'front','dist')
]

#配置上传文件的保存路径
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')



#设置上传到七牛云
QINIU_ACCESS_KEY = 'DB9RkW4Lvfk9y3PurTMWLGaNyIUI4CE0KdorbpAw'
QINIU_SECRET_KEY = 'ZHFDIs4ZabIGx9l_RSGGpLh5d3N3LBuZM-uDZ2Nr'
QINIU_BUCKET_NAME = 'hdvideo'
QINIU_DOMAIN = 'http://ps0j0p5j6.bkt.clouddn.com'

#文件上传地址必须要配置一个
UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = QINIU_ACCESS_KEY
UEDITOR_QINIU_SECRET_KEY = QINIU_SECRET_KEY
UEDITOR_QINIU_BUCKET_NAME = QINIU_BUCKET_NAME
UEDITOR_QINIU_DOMAIN = QINIU_DOMAIN

#使用ueditor文件上传到本地
UEDITOR_UPLOAD_TO_SERVER = True
UEDITOR_UPLOAD_PATH = MEDIA_ROOT
#ueditor配置文件
UEDITOR_CONFIG_PATH = os.path.join(BASE_DIR,'front','dist','ueditor','config.json')


#配置新闻首页一次加载几篇文章
ONE_PAGE_NEWS_COUNT= 2

# django-debug-toolbar配置信息
INTERNAL_IPS = ['127.0.0.1']
DEBUG_TOOLBAR_PANELS = [
    # 查看django版本
    # 'debug_toolbar.panels.versions.VersionsPanel',
    # 计时,显示当前页面加载所用时间
    'debug_toolbar.panels.timer.TimerPanel',
    # 读取django中的配置信息
    # 'debug_toolbar.panels.settings.SettingsPanel',
    # 显示当前页面的请求头和响应头信息
    # 'debug_toolbar.panels.headers.HeadersPanel',
    # 当前页面请求的详细信息(视图函数\cookie\session)
    # 'debug_toolbar.panels.request.RequestPanel',
    # 显示渲染页面所需的sql语句
    'debug_toolbar.panels.sql.SQLPanel',
    # 静态文件
    # 'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    # 模板文件
    # 'debug_toolbar.panels.templates.TemplatesPanel',
    # 缓冲信息
    # 'debug_toolbar.panels.cache.CachePanel',
    # 信号
    # 'debug_toolbar.panels.signals.SignalsPanel',
    # 日志
    # 'debug_toolbar.panels.logging.LoggingPanel',
    # 重定向
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
]
DEBUG_TOOLBAR_CONFIG= {
    'JQUERY_URL':''
}

