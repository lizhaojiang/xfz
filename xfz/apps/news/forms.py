from django.forms import Form
from apps.forms import FormMixin
from django import forms


class PublicCommentForm(forms.Form,FormMixin):
    content = forms.CharField() #评论内容
    news_id = forms.IntegerField() #被评论的新闻id