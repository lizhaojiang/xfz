from apps.forms import FormMixin
from django import forms
from apps.news.models import News


class EditNewsCategoryForm(forms.Form):
    """
    修改新闻分类表单验证
    """
    pk = forms.IntegerField(error_messages={'required':'分类id必须传递!'})
    name = forms.CharField(max_length=100)

class WriteNewsForm(forms.ModelForm,FormMixin):
    """
    添加新闻验证表单,引用需要验证的News模型
    """
    category = forms.IntegerField()
    class Meta:
        model = News
        #排除法去除不需要验证的字段
        exclude = ['category','author','pub_time']

