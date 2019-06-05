from apps.course.models import Course
from apps.forms import FormMixin
from django import forms
from apps.news.models import News
from apps.news.models import Banner


class EditNewsCategoryForm(forms.Form):
    """
    修改新闻分类表单验证
    """
    pk = forms.IntegerField(error_messages={'required': '分类id必须传递!'})
    name = forms.CharField(max_length=100)


class WriteNewsForm(forms.ModelForm, FormMixin):
    """
    添加新闻验证表单,引用需要验证的News模型,FormMixin是表单验证错误输出错误信息
    """
    category = forms.IntegerField()

    class Meta:
        model = News
        # 排除法去除不需要验证的字段
        exclude = ['category', 'author', 'pub_time']


class EditNewsForm(forms.ModelForm, FormMixin):
    category = forms.IntegerField()
    pk = forms.IntegerField()

    class Meta:
        model = News
        exclude = ['category', 'author', 'pub_time']


class AddBannerForm(forms.ModelForm, FormMixin):
    """
    添加轮播图
    """

    class Meta:
        model = Banner
        fields = ('priority', 'link_to', 'image_url')


class EditBannerForm(forms.ModelForm, FormMixin):
    """
    修改轮播图
    """
    pk = forms.IntegerField()

    class Meta:
        model = Banner
        fields = ('priority', 'link_to', 'image_url')

class PubCourseForm(forms.ModelForm,FormMixin):
    category_id = forms.IntegerField()
    teacher_id = forms.IntegerField()
    class Meta:
        model = Course
        exclude = ("category",'teacher')

