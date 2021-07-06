from django.contrib import admin
from .models import Coach,Team,Game,Player,Playergame

# Register your models here.
class coach_detail(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('name', 'teamid')
    # 设置过滤选项
    list_filter = ('name','teamid', )
    
class team_detail(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('name', 'city','numwin','numloss','ranking')
    # 设置过滤选项
    list_filter = ('name','city','ranking' )

class player_detail(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('name', 'role','city','teamid')
    # 设置过滤选项
    list_filter = ('name','role','city','teamid' )
    # 每页显示条目数 缺省值100
    list_per_page = 20

class game_detail(admin.ModelAdmin):
    # 设置页面可以展示的字段
    list_display = ('time', 'awayteamid','awayscore','hometeamid','homescore')
    # 设置过滤选项
    list_filter = ('time','awayteamid','hometeamid' )
    # 每页显示条目数 缺省值100
    list_per_page = 20

class playergame_detail(admin.ModelAdmin):
    # 每页显示条目数 缺省值100
    list_per_page = 20
    # 解决外键加载负载问题
    raw_id_fields = ('gameid','playerid')
    # 排序方式 后添加的排在前，防止添加错误
    ordering = ('-playergameid',)

# 注册model
admin.site.register(Coach,coach_detail)
admin.site.register(Team,team_detail)
admin.site.register(Player,player_detail)
admin.site.register(Game,game_detail)
admin.site.register(Playergame,playergame_detail)

# 修改管理后台名称
admin.site.site_header = '管理后台'
admin.site.site_title = '管理后台'
