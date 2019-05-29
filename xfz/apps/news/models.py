from django.db import models

#分类模型
class NewsCategory(models.Model):
    #分类名称
    name = models.CharField(max_length=100)

#新闻内容模型
class News(models.Model):

    title = models.CharField(max_length=200) #新闻标题
    desc = models.CharField(max_length=200) #新闻描述
    thumbnail = models.URLField() #缩略图
    content = models.TextField() #内容
    pub_time = models.DateTimeField(auto_now_add=True) #发布事件
    category = models.ForeignKey('NewsCategory',on_delete=models.SET_NULL,null=True) #分类引用外键
    author = models.ForeignKey('xfzauth.User',on_delete=models.SET_NULL,null=True) #作者分类 引用外键

    class Meta:
        ordering = ['-pub_time']


#评论
class Comment(models.Model):
    content = models.TextField() #评论内容
    pub_time = models.DateTimeField(auto_now_add=True) #评论发布时间
    news = models.ForeignKey('News',on_delete=models.CASCADE,related_name='comments') #评论的新闻
    author = models.ForeignKey('xfzauth.User',on_delete=models.CASCADE) #评论人

    class Meta:
        ordering = ['-pub_time']