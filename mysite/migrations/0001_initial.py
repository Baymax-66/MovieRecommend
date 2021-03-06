# Generated by Django 2.2.4 on 2019-09-10 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movies',
            fields=[
                ('MovieID', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='电影ID')),
                ('MovieName', models.CharField(max_length=200, verbose_name='电影名')),
                ('Hours', models.IntegerField(verbose_name='时长(min)')),
                ('ProduceYear', models.IntegerField(default=2020, verbose_name='生产时间')),
                ('Rating', models.FloatField(default=0.0, verbose_name='评分')),
                ('SearchTimes', models.IntegerField(default=0, verbose_name='搜索次数')),
                ('LikeTimes', models.IntegerField(default=0, verbose_name='喜欢人数')),
                ('digest', models.TextField(default='无', max_length=500, verbose_name='简介')),
            ],
        ),
        migrations.CreateModel(
            name='MovieType',
            fields=[
                ('TypeID', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('TypeName', models.CharField(max_length=12, verbose_name='电影分类')),
            ],
        ),
        migrations.CreateModel(
            name='WorkType',
            fields=[
                ('WorkID', models.CharField(max_length=5, primary_key=True, serialize=False, verbose_name='工作ID')),
                ('WorkName', models.CharField(max_length=20, verbose_name='工作名字')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('UserID', models.CharField(max_length=12, primary_key=True, serialize=False, verbose_name='用户ID')),
                ('UserName', models.CharField(max_length=30, null=True, verbose_name='用户名')),
                ('Age', models.CharField(max_length=20, null=True, verbose_name='年龄')),
                ('Gender', models.CharField(max_length=10, null=True)),
                ('Password', models.CharField(max_length=20, null=True, verbose_name='密码')),
                ('WorkID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.WorkType')),
            ],
        ),
        migrations.CreateModel(
            name='SearchLogging',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rating', models.IntegerField(verbose_name='评分')),
                ('LikeOrDislike', models.CharField(max_length=4, verbose_name='是否喜欢')),
                ('MovieID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Movies')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.User')),
            ],
        ),
        migrations.CreateModel(
            name='MovieLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MovieID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Movies')),
                ('TypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.MovieType')),
            ],
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MovieID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.Movies')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mysite.User')),
            ],
        ),
        migrations.AddIndex(
            model_name='searchlogging',
            index=models.Index(fields=['UserID', 'MovieID'], name='mysite_sear_UserID__289a5b_idx'),
        ),
        migrations.AddIndex(
            model_name='searchlogging',
            index=models.Index(fields=['UserID'], name='MovieID'),
        ),
    ]
