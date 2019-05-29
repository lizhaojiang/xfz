from rest_framework import serializers
from .models import News,NewsCategory,Comment
from apps.xfzauth.serializers import UserSerializer

"""
使用rest_framework创建序列化数据
因为category和author都是引用外键 所以需要单独创建序列化文件
"""

class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ('id','name')

# 新闻首页序列化,category\author都是外键,所以category和author也要创建自己的序列化类
class NewsSerializer(serializers.ModelSerializer):
    category = NewsCategorySerializer()
    author = UserSerializer()
    class Meta:
        model = News
        fields = ('id','title','desc','thumbnail','category','author','pub_time')


# 新闻详情页序列化,author为外键,所以要引用author的序列化类
class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('id','content','author','pub_time')