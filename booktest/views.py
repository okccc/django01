"""
视图是MVT框架的核心：接收请求(V)-->获取数据(M)-->返回结果(T)
Django通过视图接收请求,通过模型获取数据,调用模板展示结果

views
1.视图是定义在views.py中的函数,接收request对象(包含请求信息)作为第一个参数,Django提供render()函数简化了视图调用模板、往模板传递数据
2.定义完视图需要配置对应的url路由,每个app都会有单独的urls.py文件,然后将各个app的urls添加到project的urls.py文件
url路由包括正则表达式和视图两部分 --> Django使用正则匹配请求的url,一旦匹配成功就会调用对应的视图
注意：正则只匹配路径部分(即去除域名和参数的字符串)
http://192.168.233.11:7777/booktest/1/?i=1&j=2 --> 只匹配booktest/1/部分
匹配过程：先与project的url路由匹配,成功后再用剩余部分与app中的url路由匹配
先拿'booktest/'匹配project中的urls.py,再拿'1/'匹配app中的urls.py
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.urlresolvers import reverse  # url反向解析
from django.conf import settings
from django.core.paginator import Paginator  # 分页
from .models import *


def index(request):
    """
    HttpRequest对象由Django自动创建,HttpResponse对象自己开发
    服务器接收http协议的请求后,会根据报文创建HttpRequest对象,并将其作为视图函数的第一个参数
    GET属性: 一个类字典对象,包含get请求方式的所有参数
    POST属性: 一个类字典对象,包含post请求方式的所有参数
    COOKIES属性: 一个标准的Python字典,包含所有的cookie,键和值都为字符串
    session属性: 一个既可读又可写的类字典对象,表示当前的会话,只有当Django启用会话时才可用,详细内容见"状态保持"
    is_ajax()方法: 如果请求是通过XMLHttpRequest发起的,则返回True
    """

    # 调通程序
    # return HttpResponse("hello")
    # 构造字典类型的上下文(要往模板中传递的数据)
    context = {"books": BookInfo.objects.all()}
    # 返回渲染后的模板
    # return HttpResponse(loader.get_template(template_name).render(context))
    return render(request, template_name="booktest/index.html", context=context)

def detail01(request, bid):
    context = {"heros": BookInfo.objects.get(id=bid).heroinfo_set.all()}
    return render(request, "booktest/detail01.html", context)

def detail02(request, bid, hid):
    # 往模板传递数据
    context = {"hero": BookInfo.objects.get(id=bid).heroinfo_set.get(id=hid)}
    # 渲染模板
    return render(request, "booktest/detail02.html", context)

def add(request):
    b = BookInfo()
    b.title = "红楼梦"
    b.pub_date = '2019-01-01'
    b.reading = 10
    b.comments = 5
    b.save()
    return redirect(to='/booktest/index')

def delete(request, num):
    b = BookInfo.objects.get(id=num)
    b.delete()
    return redirect(to='/booktest/index')

def areas01(request):
    area = AreaInfo.objects.get(title='常州市')
    parent = area.parent
    children = area.areainfo_set.all()
    context = {"area": area, "parent": parent, "children": children}
    return render(request, "booktest/areas01.html", context)

def template01(request):
    """
    变量{{ variable }}
    标签{% tag %}
    过滤器{{ variable|filter }}
    注释{#...#}
    """
    # 变量{{key.value}}前面的key可能是字典、对象或列表
    dict_data = {"title": "这是字典"}
    object_data = BookInfo.objects.get(id=1)
    list_data = [1, 2, 3]
    context1 = {"dict_data": dict_data, "list_data": list_data, "object_data": object_data}
    # 单行注释{# #} 多行注释{# comment #}{# endcomment #}
    books = BookInfo.objects.all()
    context2 = {"books": books}
    return render(request, "booktest/template.html", context2)

def inherit(request):
    """模板继承"""
    return render(request, "booktest/child.html", )

def escape(request):
    """html转义"""
    # 模板对上下文传递的字符串进行输出时会转义 < > 等字符,显式的是原生字符串
    return render(request, "booktest/escape.html", {"context": "<h1>hello</h1>"})

def cookie01(request):
    """
    http协议是无状态的,客户端与服务器使用套接字通信完成之后会关闭当前socket连接,所以每次通信都是一次新的会话而不会记得之前的通信状态
    可以通过cookie或session两种方式实现会话保持,会话保持的目的是在一段时间内跟踪请求者的状态从而实现跨页面访问当前请求者的数据
    cookie：适用于记住用户名这种安全性不高的场景
    session：适用于账号密码、余额、等级、验证码等安全性较高的场景
    """
    response = HttpResponse("cookie测试")
    # 设置cookie
    response.set_cookie(key='k1', value='v1', max_age=7*24*3600)
    # 删除cookie
    response.delete_cookie(key='k1')
    return response

def session01(request):
    # 设置session键值对
    request.session["username"] = "grubby"
    request.session["age"] = 18
    # 设置过期时间：默认两周,0表示关闭浏览器失效
    request.session.set_expiry(5)
    # 删除指定session_key的session_data值
    del request.session["age"]
    # 清空所有session_key的session_data值
    request.session.clear()
    # 删除所有session_key,并删除Cookie中的sessionid
    request.session.flush()
    return HttpResponse("session测试")

def login(request):
    """显示登录页面"""
    # 先判断是否是已登录用户
    if "is_login" in request.session:
        # 已登录直接跳转到首页
        return redirect(to=reverse('booktest:index'))
    else:
        # 未登录,看看是否记住用户名
        if "username" in request.COOKIES:
            username = request.COOKIES.get("username")
        else:
            username = ""
        # 报错：You called this URL via POST, but the URL doesn't end in a slash and you have APPEND_SLASH set
        # 原因：form表单提交的action路径要和URL路由对应的正则保持格式一致,即是否以/结尾
        return render(request, "booktest/login.html", {"username": username})

def login_check(request):
    """处理登录校验"""
    print(request.method)  # POST
    print(type(request.POST))  # <class 'django.http.request.QueryDict'>
    # 获取form表单数据
    # request对象的GET/POST请求返回的是QueryDict对象,类似字典但是允许一键多值的情况
    # get()返回单个值,如果有多个值就取最后一个  getlist()返回列表
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    # 对比验证码
    code1 = request.POST.get('verify_code')
    code2 = request.session.get('verify_code')
    if code1.upper() != code2.upper():
        # 验证码错误,重新登录
        return redirect(to=reverse('booktest:login'))
    # 校验用户名和密码
    if username == "aaa" and password == "123":
        # 登陆成功
        # 注意：redirect、href、action的path要以/开头表示绝对路径http://ip:port/path,不然是相对路径http://ip:port/current_path/path
        response = redirect(to=reverse('booktest:index'))
        # 判断是否点击了记住用户名复选框
        if remember == "on":
            response.set_cookie("username", username, max_age=7*24*3600)
        # 记住该用户名及其登录状态
        request.session["username"] = username
        request.session["is_login"] = True
        return response
    else:
        # 登陆失败
        return redirect(to=reverse('booktest:login'))

def login_ajax(request):
    """显式ajax登录页面"""
    return render(request, "booktest/login_ajax.html")

def login_ajax_check(request):
    """ajax登录校验"""
    print(request.method)
    # 获取用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 进行校验,返回json数据
    if username == 'grubby' and password == 'grubby':
        # 用户名密码正确
        # return redirect('/index')  ajax请求都在后台,不能返回页面或者重定向,必须返回JsonResponse()
        return JsonResponse({'res': 1})
    else:
        # 用户名或密码错误
        return JsonResponse({'res': 0})

# 很多页面是必须登录之后才能访问,可以将登录判断功能封装成装饰器,用来装饰那些需要登录后才能执行的视图函数
def login_required(func):
    def wrapper(request, *args, **kwargs):
        # 判断用户是否登录
        if "is_login" in request.session:
            # 已登录,调用对应视图函数
            return func(request, *args, **kwargs)
        else:
            # 未登录,跳转到登录页面
            return redirect(to=reverse('booktest:login'))
    return wrapper

@login_required
def change_pwd(request):
    """显式修改密码页面"""
    return render(request, "booktest/change_pwd.html")

@login_required
def change_pwd_check(request):
    """处理修改密码"""
    print(request.method)
    password = request.POST.get('password')
    username = request.session.get('username')
    # 实际开发应该是修改数据库内容
    return HttpResponse("%s修改密码为%s" % (username, password))

from PIL import Image, ImageDraw, ImageFont
from django.utils.six import BytesIO
import random
def verify_code(request):
    """
    在用户登录注册页面,为了防止暴力请求可以加入验证码功能
    报错：OSError: cannot open resource
    原因：linux上没有truetype字体,从windows拷几个到/usr/share/fonts目录下即可
    """

    # 定义变量,用于画面的背景色、宽、高 RGB
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'abcdABCD123efghijkEFGHIJK456lmnopqrsLMNOPQRS789TUVWXYZ0tuvwxyz'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象,ubuntu的字体路径为/usr/share/fonts/truetype/freefont
    font = ImageFont.truetype('msyhbd.ttc', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session,用于做进一步验证
    request.session['verify_code'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片保存在内存中,文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端,MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def static01(request):
    """静态文件"""
    # 静态文件查找顺序
    print(settings.STATICFILES_FINDERS)
    # ['django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder']
    # 拦截ip,可以用装饰器或者在django的中间件实现
    # ip = request.META['REMOTE_ADDR']
    # if ip == '192.168.152.1':
    #     return HttpResponse('<h1>forbidden<h1>')
    return render(request, "booktest/static01.html")

def upload(request):
    """显式上传页面"""
    return render(request, "booktest/upload.html")

def upload_handler(request):
    """上传文件"""
    # 获取form表单数据
    picture = request.FILES["pic"]
    # print(type(picture))
    # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>  # 上传文件<2.5M放在内存中
    # <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>  # 上传文件>2.5M放在临时文件中
    # 读取文件内容并保存到上传文件目录
    filename = "%s/booktest/%s" % (settings.MEDIA_ROOT, picture.name)
    # print(filename)
    with open(filename, "wb") as f:
        # chunks()返回生成器,取代read()防止文件太大占用过多内存
        for content in picture.chunks():
            f.write(content)
    # 在数据库中保存上传记录
    Picture.objects.create(picture="booktest/%s" % picture.name)
    return HttpResponse("ok")

def paging(request, pindex):
    """分页"""
    # 获取所有省份信息
    provinces = AreaInfo.objects.filter(parent__isnull=True)
    # 将该数据设置成每页显示10条
    paginator = Paginator(provinces, 10)
    # 分页后的页码总数
    # print(paginator.num_pages)  # 4
    # 分页后的页码列表
    # print(paginator.page_range)  # range(1, 5)
    # 获取第pindex页数据
    if pindex == "":
        pindex = 1
    else:
        pindex = int(pindex)
    page_index = paginator.page(pindex)
    # 往模板传数据
    context = {"page": page_index}
    # 渲染模板
    return render(request, "booktest/paging.html", context=context)

def areas02(request):
    """省市县下拉框"""
    return render(request, "booktest/areas02.html")

def prov(request):
    """获取所有省级地区的信息"""
    # 1.获取所有省级地区的信息
    areas = AreaInfo.objects.filter(parent__isnull=True)
    # 2.遍历areas并拼接出json数据：id title
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.title))
    # 3.返回数据
    return JsonResponse({'data': areas_list})

def city(request, pid):
    """获取pid的下级地区的信息"""
    # 1.获取pid对应地区的下级地区
    areas = AreaInfo.objects.filter(parent__id=pid)
    # 2.遍历areas并拼接出json数据：id title
    areas_list = []
    for area in areas:
        areas_list.append((area.id, area.title))
    # 3.返回数据
    return JsonResponse({'data': areas_list})




