from django import forms
from apps.forms import FormMixin
from django.core.cache import cache
from .models import User


#登录表单验证
class LoginForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11,error_messages={"max_length":"请填写正确的手机号!"})
    password = forms.CharField(max_length=16,min_length=6,error_messages={"max_length":"密码最大长度16位","min_length":"密码不能少于6位"})
    remember = forms.IntegerField(required=False)


#注册表单验证
class RegisterForm(forms.Form,FormMixin):
    telephone = forms.CharField(max_length=11)
    username = forms.CharField(max_length=20)
    password1 = forms.CharField(max_length=16,min_length=6,error_messages={"max_length":"密码最大长度16位","min_length":"密码不能少于6位"})
    password2 = forms.CharField(max_length=16,min_length=6,error_messages={"max_length":"密码最大长度16位","min_length":"密码不能少于6位"})
    img_captcha = forms.CharField(max_length=4,min_length=4)
    sms_captcha = forms.CharField(max_length=6,min_length=6)

    # 验证两次密码是否一致,图形和短信验证码是否在缓冲中存在
    # 重写父类的clean方法,成功返回cleaned_data数据 失败返回异常
    def clean(self):
        #调用父类方法
        cleaned_data = super(RegisterForm, self).clean()

        #获取验证的数据
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        #验证密码
        if password1 != password2:
            raise forms.ValidationError('两次密码输入不一致!')

        #获取用户和缓冲读取的验证码

        #验证图形验证码
        img_captcha = cleaned_data.get('img_captcha')
        captcha_img_captcha = cache.get(img_captcha.lower())
        #验证验证码
        if not captcha_img_captcha or img_captcha.lower() != captcha_img_captcha.lower():
            raise forms.ValidationError('图形验证码有误!')

        #验证短信验证码
        telephone = cleaned_data.get('telephone')
        sms_captcha = cleaned_data.get('sms_captcha')
        captcha_sms_captcha = cache.get(telephone)

        if not captcha_sms_captcha or sms_captcha != captcha_sms_captcha:
            raise forms.ValidationError('手机验证码有误!')

        #验证手机号是否存在,数据库中手机号唯一
        exists = User.objects.filter(telephone=telephone).exists()
        if exists:
            raise forms.ValidationError('手机号已经注册!')


