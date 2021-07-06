from django.db import models

# 根据需求分析，建立合适表

class Team(models.Model):
    teamid = models.AutoField('队伍编号',primary_key=True)
    name = models.CharField('名称',max_length=20)
    numwin = models.IntegerField('胜场数')
    numloss = models.IntegerField('负场数')
    ranking = models.IntegerField('排名')
    city = models.CharField('区域',max_length=30)

    def __str__(self):
        return str(self.city)+':'+str(self.name)
        
    class Meta:
        db_table = 'team'
        verbose_name = '队伍'
        verbose_name_plural = '队伍'
        
class Coach(models.Model):
    coachid = models.AutoField('教练编号',primary_key=True)
    name = models.CharField('姓名',max_length=20)
    teamid = models.ForeignKey(Team,on_delete = models.PROTECT, db_column='teamid', verbose_name='执教队伍')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        db_table = 'coach'
        verbose_name = '教练'
        verbose_name_plural = '教练'

class Player(models.Model):
    ROLE_CHOICES = [
        ('中锋','中锋'),
        ('前锋','前锋'),
        ('后卫','后卫'),
    ]
    
    playerid = models.AutoField('球员编号',primary_key=True)
    name = models.CharField('姓名',max_length=20)
    role = models.CharField('位置',choices = ROLE_CHOICES,max_length=10)
    city = models.CharField('城市',max_length=40)
    teamid = models.ForeignKey(Team,on_delete = models.PROTECT, db_column='teamid',verbose_name='效力队伍')

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name = '球员'
        verbose_name_plural = '球员'
        db_table = 'player'

class Game(models.Model):
    gameid = models.AutoField('赛事编号',primary_key=True)
    hometeamid = models.ForeignKey(Team,on_delete=models.PROTECT,related_name='hometeam_f', db_column='hometeamid',verbose_name='主场队伍')
    homescore = models.IntegerField('主场得分')
    awayteamid = models.ForeignKey(Team,on_delete=models.PROTECT, related_name='awayteam_f',db_column='awayteamid',verbose_name='客场队伍')
    awayscore = models.IntegerField('客场得分')
    homeplayers = models.IntegerField('主场队伍球员数')
    awayplayers = models.IntegerField('客场队伍球员数')
    time = models.DateField('比赛时间',blank=True, null=True)

    def __str__(self):  
        return str(self.time)+':'+str(self.hometeamid.name)+' vs '+str(self.awayteamid.name)
        
    class Meta:
        db_table = 'game'
        verbose_name = '赛事'
        verbose_name_plural = '赛事'





class Playergame(models.Model):
    
    ISFIRST_CHOICES = [
        (0,"否"),
        (1,"是"),
    ]
    ISHOME_CHOICES = [
        (0,"否"),
        (1,"是"),
    ]
    playergameid = models.AutoField(primary_key=True)
    gameid = models.ForeignKey(Game, on_delete = models.PROTECT, db_column='gameid',verbose_name='比赛')
    playerid = models.ForeignKey(Player, on_delete= models.PROTECT, db_column='playerid',verbose_name='球员')
    isfirst = models.IntegerField('是否首发',choices=ISFIRST_CHOICES)
    time = models.IntegerField('上场时间')
    pts = models.IntegerField('得分')
    athome = models.IntegerField('是否主场',choices=ISHOME_CHOICES)

    class Meta: 
        db_table = 'playergame'
        unique_together = ('gameid', 'playerid')
        verbose_name = '技术统计信息'
        verbose_name_plural = '技术统计信息'
        
    def __str__(self):
        return str(self.gameid) + ' 中 ' + str(self.playerid.name) + ' 的表现'
    


