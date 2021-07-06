from django.conf.urls import url
from . import views
from django.contrib import admin


app_name = 'backend'

# 使用正则表达式来获取url中所包含的参数，以正确显示球员，教练，队伍的信息
urlpatterns = [
    url(r'^$', views.index, name='index'),

    # /teams/
    url(r'^teams/$', views.teams_overview, name='teams_overview'),

    # /coaches/
    url(r'^coaches/$', views.coaches_overview, name='coaches_overview'),

    # /players/
    url(r'^players/$', views.players_overview, name='players_overview'),

    # /games/
    url(r'^games/$', views.games_overview, name='games_overview'),

    # /team/<teamid>
    url(r'^team/(?P<teamid>[0-9]+)/$', views.team_detail, name='team_detail'),
    
    # /coach/<coachid>
    url(r'^coach/(?P<coachid>[0-9]+)/$', views.coach_detail, name='coach_detail'),

    # /player/<playerid>
    url(r'^player/(?P<playerid>[0-9]+)/$', views.player_detail, name='player_detail'),

    # /game/<gameid>
    url(r'^game/(?P<gameid>[0-9]+)/$', views.game_detail, name='game_detail'),

    url(r'^forms/players/$', views.PlayersFormView.as_view(), name='players_query'),

    url(r'^forms/games/$', views.GamesFormView.as_view(), name='games_query'), 
    
    url('analyse',views.analyse,name='analyse'),

]