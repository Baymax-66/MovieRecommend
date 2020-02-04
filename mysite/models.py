from django.db import models


class WorkType(models.Model):
    WorkID = models.CharField("工作ID", max_length=5,primary_key=True)
    WorkName = models.CharField("工作名字",max_length=20)


class User(models.Model):
    UserID = models.CharField('用户ID', max_length=12,primary_key=True)
    UserName = models.CharField('用户名', max_length=30,null=True)
    Age = models.CharField('年龄',max_length=20,null=True)
    Gender = models.CharField(max_length=10,null=True)
    Password = models.CharField('密码', max_length=20,null=True)
    # WorkName = models.CharField('职业分类', max_length=12)
    WorkID = models.ForeignKey(WorkType, on_delete=models.CASCADE)


class Movies(models.Model):
    MovieID = models.CharField('电影ID', max_length=12, primary_key=True)
    MovieName = models.CharField('电影名', max_length=200)
    Hours = models.IntegerField('时长(min)')
    ProduceYear = models.IntegerField('生产时间', default=2020)
    # Country = models.CharField('生产地', max_length=20)
    Rating = models.FloatField('评分', default=0.0)
    SearchTimes = models.IntegerField('搜索次数', default=0)
    LikeTimes = models.IntegerField('喜欢人数', default=0)
    # Url = models.URLField('链接地址', default='https://www.baidu.com/img/bd_logo1.png?qua=high&where=super')
    digest = models.TextField("简介", default='无', max_length=500)


class MovieType(models.Model):
    TypeID = models.CharField(primary_key=True, max_length=5)
    TypeName = models.CharField('电影分类', max_length=12)


class MovieLabel(models.Model):
    MovieID = models.ForeignKey(Movies, on_delete=models.CASCADE)
    TypeID = models.ForeignKey(MovieType, on_delete=models.CASCADE)


class SearchLogging(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    MovieID = models.ForeignKey(Movies, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['UserID', 'MovieID']),
            models.Index(fields=['UserID'], name='MovieID'),
        ]

    Rating = models.IntegerField('评分')
    LikeOrDislike = models.CharField('是否喜欢', max_length=4)


class Collect(models.Model):
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    MovieID = models.ForeignKey(Movies, on_delete = models.CASCADE)


