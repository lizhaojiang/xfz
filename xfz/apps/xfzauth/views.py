from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout,authenticate
from django.views.decorators.http import require_POST
from .forms import LoginForm,RegisterForm
from django.http import JsonResponse,HttpResponse
from utils import restful
from utils.captcha.xfzcaptcha import Captcha
from io import BytesIO
from utils.aliyunsdk import aliyunsms
from utils import restful
from django.core.cache import cache
import random

#导入这个方法是为了获取settings中的指定User
from django.contrib.auth import get_user_model
User = get_user_model()


#使用require_POST装饰函数,只能接受post请求
@require_POST
def login_view(request):
    #创建表单实例
    form = LoginForm(request.POST)
    #验证表单信息,并且获取表单内容
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember')

        #使用django自带authenticate方法,验证登录,正确返回user对象,不正确返回None
        user = authenticate(request,username=telephone, password=password)

        #登录成功后继续执行
        if user:
            #判断是否进入黑名单
            if user.is_active:
                #使用login方法保持会话状态
                login(request,user)
                #如果用户选择记住密码,设置过期时间为默认的两周,否则浏览器关闭即过期
                if remember:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
                #登录返回json数据,登录成功返回200,使用通用格式
                return restful.result()
            else: #如果是黑名单,则返回405 表示没有权限,或者是其他错误
                return restful.unauth(message="没有权限")
        else: #验证失败,登录信息错误
            return restful.params_error(message="手机号或者密码错误!")
    else: #表单验证错误
        errors = form.get_errors()
        return restful.params_error(message=errors)

#退出登录
def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

def img_captcha(request):
    # 生成验证码内容和图片
    text,image = Captcha.gene_code()
    # 返回图片,response无法返回图片,需要使用io中的BytesIO
    out = BytesIO()
    # 将图片保存到数据流,并且需要定义返回类型
    image.save(out,'png')
    # 将文件指针移动到最开始的位置
    out.seek(0)
    # 指定返回的类型为图片类型, 大类/小类
    response = HttpResponse(content_type='image/png')
    # 从BytesIO管道中读取图片数据,保存到response中
    response.write(out.read())
    # 获取文件指针的位置
    response['Content-length'] = out.tell()

    # 将生成的验证码保存到memcached缓冲中
    # 参数分别是 key value expiry
    cache.set(text.lower(),text.lower(),5*60)

    # 返回response
    return response

#注册
@require_POST
def register(request):
    #创建form表单实例
    form = RegisterForm(request.POST)
    #验证表单,获取表单信息
    if form.is_valid():
        telephone = form.cleaned_data.get('telephone')
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        #保存用户
        user = User.objects.create_user(telephone=telephone,username=username,password=password)
        #保持会话状态
        login(request,user)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_errors())



#短信验证
def sms_captcha(request):
    # 获取手机号
    telephone = request.GET.get('telephone')
    # 生成随机验证码,使用图形验证码里面的方法
    # code = Captcha.gene_text()
    code = '%06d'%random.randint(0,999999)

    #将手机号验证码保存到memcached中
    cache.set(telephone,code,5*60)

    # 发送短信,接受并返回
    aliyunsms.send_sms(telephone,code)

    print("短信验证码:",code)
    return restful.ok()


def cache_test(request):
    cache.set('username','lizhaojiang',60)
    result = cache.get('username')
    print(result)
    return HttpResponse('success')



