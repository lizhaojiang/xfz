from django.http import JsonResponse

#定义返回的参数
class HttpCode(object):
    ok = 200            #正确
    paramserror = 400   #参数错误
    unauth = 401        #权限不够
    methoderror = 405   #请求方法错误
    servererror = 500   #服务器错误


#封装方法返回的值code(返回的状态码,默认成功),message(返回的错误信息,默认空),data(返回信息,默认空)
def result(code=HttpCode.ok,message='',data=None,kwargs=None):
    # 定义一个返回数据
    json_dict = {'code':code,'message':message,'data':data}
    # 如果kwargs存在,并且是字典类型,并且key有值
    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        #使用update将一个字典添加到另一个字典中
        json_dict.update(kwargs)

    return JsonResponse(json_dict)

def ok():
    return result()

#参数错误
def params_error(message='',data=None):
    return result(code=HttpCode.paramserror,message=message,data=data)

#没有权限
def unauth(message="",data=None):
    return result(code=HttpCode.unauth,message=message,data=data)

#请求方法错误
def method_error(message="",data=None):
    return result(code=HttpCode.methoderror,message=message,data=data)

#服务器内部错误
def server_error(message="",data=None):
    return result(code=HttpCode.servererror,message=message,data=data)


