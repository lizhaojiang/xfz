from django.urls import path
from . import views

#设置命名空间
app_name = 'course'

urlpatterns = [
    path('',views.course_index,name='course_index'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
]