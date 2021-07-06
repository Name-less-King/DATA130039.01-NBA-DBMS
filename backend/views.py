# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from django.db.models import Count, Avg

from .models import Team, Player, Game, Coach, Playergame
from .forms import PlayersForm, GamesForm


# Create your views here.

# 主视图
def index(request):
    return render(request, 'nba/index.html')

# 数据分析视图
def analyse(request):
    return render(request, 'nba/analyse.html')
# 队伍整体浏览视图，分区排放较为美观,按照排名摆放也方便用户
def teams_overview(request):
    # Get all the teams in the NBA
    teams_nw = Team.objects.filter(city = '西北区').order_by('ranking')
    teams_m = Team.objects.filter(city = '中区').order_by('ranking')
    teams_p = Team.objects.filter(city = '太平洋区').order_by('ranking')
    teams_a = Team.objects.filter(city = '大西洋区').order_by('ranking')
    teams_se = Team.objects.filter(city = '东南区').order_by('ranking')
    teams_sw = Team.objects.filter(city = '西南区').order_by('ranking')
    return render(request, 'nba/teams_overview.html', {'nw': teams_nw,'m': teams_m,
                                                       'p': teams_p,'a': teams_a,
                                                       'se': teams_se,'sw': teams_sw})

# 总体视图，加入分页特性，更加美观，也使得加载更快
def coaches_overview(request):
    # Get all the coaches in the NBA    
    coach_list = Coach.objects.all().order_by('coachid')
    # paginator 分页器需要两个参数,一个object_list  一个 per_page
    paginator = Paginator(coach_list, 15)
    # 去前端拿到对应的页数
    current_page_num = int(request.GET.get('page', 1))
 
    if paginator.num_pages > 1:
        if current_page_num - 5 < 1:
            # 这里写的（1， 3） 是我们要显示2个按钮
            page_range = range(1, 3)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
        else:
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range
 
    try:
        coaches = paginator.page(current_page_num)
        
    except EmptyPage as e:
        # 如果出现的是负数，或者大于页码的数，我们默认让其显示第一页
        coaches = paginator.page(1)
 
    return render(request,'nba/coaches_overview.html',{'coaches':coaches,'page_range':page_range})

def players_overview(request):
    # Get all the players who played in the NBA in 2018-19 season
    players_list = Player.objects.all().order_by('playerid')
    # paginator 分页器需要两个参数,一个object_list  一个 per_page
    paginator = Paginator(players_list, 15)
    # 去前端拿到对应的页数
    current_page_num = int(request.GET.get('page', 1))
 
    if paginator.num_pages > 1:
        if current_page_num - 5 < 1:
            # 这里写的（1， 11） 是我们要显示10个按钮
            page_range = range(1, 11)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
        else:
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range
 
    try:
        players = paginator.page(current_page_num)
        
    except EmptyPage as e:
        # 如果出现的是负数，或者大于页码的数，我们默认让其显示第一页
        players = paginator.page(1)
    return render(request, 'nba/players_overview.html', {'players': players,'page_range': page_range})

def games_overview(request):
    # Get all the games from the 2018-19 season
    games_list = Game.objects.all().order_by('-time')
    # paginator 分页器需要两个参数,一个object_list  一个 per_page
    paginator = Paginator(games_list, 15)
    # 去前端拿到对应的页数
    current_page_num = int(request.GET.get('page', 1))
 
    if paginator.num_pages > 1:
        if current_page_num - 5 < 1:
            # 这里写的（1， 11） 是我们要显示10个按钮
            page_range = range(1, 11)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)
        else:
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range
 
    try:
        games = paginator.page(current_page_num)
        
    except EmptyPage as e:
        # 如果出现的是负数，或者大于页码的数，我们默认让其显示第一页
        games = paginator.page(1)
    return render(request, 'nba/games_overview.html', {'games': games,'page_range': page_range})

# 为每一个具体的实体定义视图
def team_detail(request, teamid):
    team = get_object_or_404(Team, pk=teamid)
    players = Player.objects.filter(teamid=teamid)
    coaches = get_list_or_404(Coach, teamid=teamid)
    return render(request, 'nba/team_detail.html', {'team': team, 'players': players, 'coaches': coaches})

def coach_detail(request, coachid):
    # Get the specific player
    coach = get_object_or_404(Coach, pk=coachid)
    
    return render(request, 'nba/coach_detail.html', {'coach': coach })

def player_detail(request, playerid):
    # Get the specific player
    player = get_object_or_404(Player, pk=playerid)

    # Get all the games the player played in
    games_played = get_list_or_404(Playergame.objects.order_by('-gameid'), playerid=playerid)
    
    return render(request, 'nba/player_detail.html', {'player': player, 'games_played': games_played})

def game_detail(request, gameid):
    
    game = get_object_or_404(Game, pk=gameid)

    # Get all players who played in this specific game
    players_away = get_list_or_404(Playergame.objects.order_by('-pts'),gameid = gameid,athome=0)
    players_home = get_list_or_404(Playergame.objects.order_by('-pts'),gameid = gameid,athome=1)
    return render(request, 'nba/game_detail.html', {'game': game, 'players_away': players_away,'players_home':players_home})

# 为表单搜索定义视图
class PlayersFormView(View):
    form_class = PlayersForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, 'nba/players_query.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if request.method == "POST":
            player_name = request.POST['player_name']
            team_name = request.POST['team_name']
            role = request.POST['role']
            player_city = request.POST['player_city']
            min_points_scored = int(request.POST['min_points_scored'])
            max_points_scored = int(request.POST['max_points_scored'])
            display = int(request.POST['display'])
            
            #整型可以直接传入，不用担心安全问题
            query = """WITH a AS (SELECT playerid,avg(pts) AS avg FROM playergame  GROUP by playerid Having avg between {} and {})
                        SELECT * FROM a LEFT JOIN player ON a.playerid = player.playerid WHERE name like %s
                        AND role like %s
                        AND teamid in (SELECT teamid FROM team WHERE name like %s)
                        AND city like %s
                        ORDER BY AVG DESC""".format(min_points_scored,max_points_scored)

            if display == 1: 
                query = query+""" LIMIT 200 """
                        
            #防止使用字符串手段进行sql注入
            player_name = '%%'+player_name+'%%'
            team_name = '%%'+team_name+'%%'
            role = '%%'+role+'%%'
            player_city = '%%'+player_city+'%%'
            
            
            #参数化查询
            players = Player.objects.raw(query,[player_name,role,team_name,player_city])
            
            # 没有找到结果则返回错误页面，给用户一些提示
            if  len(list(players)) !=0:
                return render(request, 'nba/results.html', {'players': players})
            else: 
                return render(request,'nba/results1_error.html')  
            
        return render(request, 'nba/forms.html', {'form': form})

class GamesFormView(View):
    form_class = GamesForm

    def get(self, request):
        form = self.form_class(None)
        return render(request, 'nba/games_query.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if request.method == "POST":
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            team_name_1 = request.POST['team_name_1']
            team_name_2 = request.POST['team_name_2']
            player_name = request.POST['player_name']
            display = int(request.POST['display'])
            
            # 不输入起止时间的话就默认一个很早和很晚的时间，对搜索结果不产生影响
            if start_time == '':
                start_time = '2010-1-1'
            if end_time == '':
                end_time = '2020-1-1'
                
            #日期格式可以直接传入，不用担心安全问题
            query = """SELECT * FROM GAME WHERE time BETWEEN '{}' AND '{}' 
            AND ( hometeamid in (SELECT teamid FROM team WHERE name like %s) OR awayteamid in (SELECT teamid FROM team WHERE name like %s) )
            AND ( hometeamid in (SELECT teamid FROM team WHERE name like %s) OR awayteamid in (SELECT teamid FROM team WHERE name like %s) )
            AND  gameid in (SELECT gameid FROM playergame WHERE playerid in (SELECT playerid FROM player WHERE name like %s)) 
            ORDER BY time DESC
                          """.format(start_time,end_time) 
            
            if display == 1:
                query = query + """ LIMIT 200"""
            
            #防止使用字符串手段进行sql注入
            team_name_1 = '%%'+team_name_1+'%%'
            team_name_2 = '%%'+team_name_2+'%%'
            player_name = '%%'+player_name+'%%'
            
            #参数化查询
            games =Game.objects.raw(query,[team_name_1,team_name_1,team_name_2,team_name_2,player_name])
            
            # 没有找到结果则返回错误页面，给用户一些提示
            if  len(list(games)) !=0:
                return render(request, 'nba/results2.html', {'games': games})
            else: 
                return render(request,'nba/results2_error.html')  
        return render(request, 'nba/forms.html', {'form': form})
