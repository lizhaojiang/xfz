from apps.forms import FormMixin
from django import forms
from .models import Teacher,CourseCategory


class EditCourseCategoryForm(forms.Form):
    """
    修改课程分类表单验证
    """
    pk = forms.IntegerField(error_messages={'required': '分类id必须传递!'})
    name = forms.CharField(max_length=100)


class WriteTeachForm(forms.ModelForm,FormMixin):
    class Meta:
        model = Teacher
        fields = ('username','avatar','jobtitle','profile')

class EditTeachForm(forms.ModelForm, FormMixin):
    pk = forms.IntegerField()
    class Meta:
        model = Teacher
        fields = ('username', 'avatar', 'jobtitle', 'profile')
