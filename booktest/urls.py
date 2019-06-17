from django.conf.urls import url
from . import views

# 配置url路由
urlpatterns = [
    # url反向解析：请求链接由namespace:name动态生成而不是手动拼接,当修改url路由的匹配规则时不需要更改模板和视图
    # 模板中的超链接：{% url 'namespace:name' p1 p2 .. %}
    # 视图中的重定向：reverse('namespace:name')
    url('^$', views.index, name='index'),
    url('^index/$', views.index, name='index'),

    # (1)位置参数：视图参数名随便指定
    url('^index/(\d+)/$', views.detail01, name='detail01'),
    url('^index/(\d+)/(\d+)/$', views.detail02, name='detail02'),
    # (2)关键字参数(?P<组名>)：视图参数名要和正则组名一致
    url('^(?P<num>\d+)/$', views.detail01, name='detail01'),

    url('^add/$', views.add, name='add'),
    url('^delete(\d+)/$', views.delete, name='delete'),
    url('^areas/$', views.areas, name='areas'),  # 地区信息

    url('^template01', views.template01, name='template01'),
    url('^inherit', views.inherit, name='inherit'),
    url('^escape', views.escape, name='escape'),

    url('^cookie01', views.cookie01, name='cookie01'),
    url('^session01', views.session01, name='session01'),
    url('^login/$', views.login, name='login'),
    url('^login_check$', views.login_check, name='login_check'),
    url('^login_ajax$', views.login_ajax, name='login_ajax'),
    url('^login_ajax_check$', views.login_ajax_check, name='login_ajax_check'),
    # 注意：url路由的正则表达式严谨的写法必须以$结尾,不然名字相似的url可能匹配不到,比如change_pwd_check其实匹配的是change_pwd
    url('^change_pwd$', views.change_pwd, name='change_pwd'),
    url('^change_pwd_check$', views.change_pwd_check, name='change_pwd_check'),

    url('^verify_code$', views.verify_code, name='verify_code'),
    url('^static01$', views.static01, name='static01'),
    url('^upload$', views.upload, name='upload'),
    url('^upload_handler$', views.upload_handler, name='upload_handler'),
    url('^paging/(\d*)$', views.paging, name='paging'),
]

