from utils import restful
from django.shortcuts import redirect


# 定义装饰器,用户是否登录返回的是json数据使用
def xfz_login_require(func):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.unauth(message='请先登录')
            else:
                return redirect('/')
    return wrapper

