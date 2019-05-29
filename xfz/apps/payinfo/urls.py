from django.urls import path
from . import views

#设置命名空间
app_name = 'payinfo'

urlpatterns = [
    path('',views.payinfo,name='payinfo'),
]