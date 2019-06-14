"""
admin站点注册模型类
Django提供了admin.ModelAdmin类,通过定义其子类来自定义模型在admin界面的显示方式,可以对model做增删改查
"""
from django.contrib import admin
from .models import BookInfo, HeroInfo, AreaInfo

# BookInfo模型类的关联对象类
class HeroTabularInline(admin.TabularInline):
    """StackedInline/TabularInline：堆放型内嵌方式/表格型内嵌方式"""
    # 指定关联对象
    model = HeroInfo
    # 设置可额外添加的对象数量
    extra = 3

# 自定义模型管理类
class BookInfoAdmin(admin.ModelAdmin):
    # 显示字段(可调整字段顺序且字段可排序)
    list_display = ['id', 'title', 'pub_date', 'reading', 'comments', 'isDelete']
    # 过滤字段(右侧会出现过滤框)
    list_filter = ['title']
    # 搜索字段(上方会出现搜索框)
    search_fields = ['title']
    # 分页
    list_per_page = 10
    # 字段分组
    fieldsets = (
        ('基础信息', {'fields': ['title']}),
        ('其它信息', {'fields': ['pub_date']}),
    )
    # 在一对多模型的一方添加关联对象
    inlines = [HeroTabularInline]


class HeroInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'introduce']


# AreaInfo模型类的关联对象类
class AreaTabularInline(admin.TabularInline):
    # 指定关联对象
    model = AreaInfo
    # 设置可额外添加的对象数量
    extra = 3

class AreaInfoAdmin(admin.ModelAdmin):
    # 显示字段(可调整字段顺序且字段可排序)
    list_display = ['id', 'title', 'parent']
    # 过滤字段(右侧会出现过滤框)
    list_filter = ['title']
    # 搜索字段(上方会出现搜索框)
    search_fields = ['title']
    # 分页
    list_per_page = 10
    # 给字段分组
    fieldsets = [
        ('基础信息', {'fields': ['parent']}),
        ('其它信息', {'fields': ['title']}),
    ]
    # 在一对多模型的一方添加关联对象
    inlines = [AreaTabularInline]
    # 设置在顶部/底部显示属性
    actions_on_bottom = True
    actions_on_top = True

# 注册模型到admin
admin.site.register(BookInfo, BookInfoAdmin)
admin.site.register(HeroInfo, HeroInfoAdmin)
admin.site.register(AreaInfo, AreaInfoAdmin)