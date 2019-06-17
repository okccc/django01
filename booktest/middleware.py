# coding=utf8
from django.http import HttpResponse

class SimpleMiddleware(object):
    """
    切面编程：在框架的某个环节添加功能而不需要更改源代码,对输入或输出进行干预,类似装饰器
    mvc框架：IOC   django：中间件
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1.调用视图函数之前执行的代码块
        # 拦截ip
        exclude_ips = ['192.168.152.11']
        ip = request.META['REMOTE_ADDR']
        if ip in exclude_ips:
            response = HttpResponse('<h1>forbiden</h1>')
        else:
            response = self.get_response(request)
        # 2.调用视图函数之后执行的代码块
        return response

    def process_exception(self, request, exception):
        """视图函数异常时调用"""
        print(exception)

# 中间件是一个独立的类
# class BlockIpsMiddleware(object):
#     """拦截ip中间件"""
#     exclude_ips = ['192.168.152.1']
#
#     def process_view(self, request, view_func, *view_args, **view_kwargs):
#         """调用视图函数之前会先调用此方法"""
#         ip = request.META['REMOTE_ADDR']
#         if ip in BlockIpsMiddleware.exclude_ips:
#             return HttpResponse('<h1>forbiden</h1>')
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         return self.get_response(request)





