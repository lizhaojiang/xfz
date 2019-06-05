from django.urls import path
from . import views

#设置命名空间
app_name = 'course'

urlpatterns = [
    path('',views.course_index,name='course_index'),
    path('<int:course_id>/', views.course_detail, name='course_detail'),
    path('course_token/', views.course_token, name='course_token'),
    path('course_order/<int:course_id>/', views.course_order, name='course_order'),
    path('teach/', views.AddTeachView.as_view(), name='teach'),
    path('edit_teach/', views.EditTeachView.as_view(), name='edit_teach'),
]