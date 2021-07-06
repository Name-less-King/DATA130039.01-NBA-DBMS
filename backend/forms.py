from django import forms
from .models import Team, Player, Playergame, Game, Coach
from datetime import datetime

# 查找球员的表单
class PlayersForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('%%','任意'),
        ('中锋','中锋'),
        ('前锋','前锋'),
        ('后卫','后卫'),
    ]
    
    DISPLAY_CHOICES = [
        (1,'是'),
        (0,'否'),
    ]
    
    player_name = forms.CharField(label = '球员名称',max_length=20, initial='%%')
    team_name = forms.CharField(label = '所在队伍',max_length=20, initial='%%')
    role = forms.ChoiceField(label = '擅长位置',choices= ROLE_CHOICES,initial = '%%')
    player_city = forms.CharField(label = '家乡城市',max_length=20,initial='%%')
    min_points_scored = forms.IntegerField(label = '最低场均得分',initial=0)
    max_points_scored = forms.IntegerField(label = '最高场均得分',initial=100)
    display = forms.ChoiceField(label = '是否只显示前200条结果',choices=DISPLAY_CHOICES,initial = 1)
    
    class Meta():
        model = Player
        fields = ['player_name', 'team_name', 'role', 'player_city','min_points_scored', 'max_points_scored','display']
    
# 查找球赛的表单    
class GamesForm(forms.ModelForm):
    DISPLAY_CHOICES = [
        (1,'是'),
        (0,'否'),
    ]
    
    start_time = forms.DateField(label = '起始时间',widget=forms.DateTimeInput(attrs={'type': 'date'}),required = False)
    end_time = forms.DateField(label = '终止时间',widget=forms.DateTimeInput(attrs={'type': 'date'}),required = False)
    team_name_1 = forms.CharField(label = '参赛球队',max_length=10, initial='%%')
    team_name_2 = forms.CharField(label = '参赛球队',max_length=10, initial='%%')
    player_name = forms.CharField(label = '参赛球员',max_length=20, initial='%%')
    display = forms.ChoiceField(label = '是否只显示前200条结果',choices=DISPLAY_CHOICES,initial = 1)
    
    class Meta():
        model = Game
        fields = ['start_time','end_time','team_name_1','team_name_2','player_name','display']