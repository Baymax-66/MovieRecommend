from django.shortcuts import render, redirect
from .forms import UserForm, RegisterForm, DetailsForm
from .models import User,WorkType,SearchLogging, Movies, MovieLabel, Collect, MovieType
from .CF import UserCf
import numpy as np


def init_rating(if_rand=True):
    """
    用来初始化所有的平均分：
    更新对象：mysite_movies.Ratings
    状态：测试中
    if_rand=True:随机生成评分
    :return:
    """

    # 如果选择随机生成就直接生成就好
    if if_rand:
        movies = Movies.objects.all()
        for m in movies:
            m.Rating = np.random.rand()*4.5
            m.save()
    # 获取每个用户对某个电影的所有评分，求出总共的评分

    data = SearchLogging.objects.all()
    tmp = {'UserID': [], 'MovieID': [], 'Rating': []}
    for e in data:
        tmp['UserID'].append(int(e.UserID_id))
        tmp['MovieID'].append(int(e.UserID_id))
        tmp['Rating'].append(float(e.Rating))

    # 记录总分，总次数
    sum_rating = np.zeros((max(tmp['MovieID']) + 1,))
    sum_times = np.zeros((max(tmp['MovieID']) + 1,))
    ave = np.zeros((max(tmp['MovieID']) + 1,))

    for i in range(len(tmp['MovieID'])):
        x = tmp['MovieID'][i]
        sum_rating[x] += tmp['Rating'][i]
        sum_times[x] += 1

    # 计算平均数
    for i in range(len(sum_times)):
        r = sum_rating[i]
        t = sum_times[i]
        if t != 0:
            ave[i] = r/t

    for x in tmp['MovieID']:
        # Movies.objects.filter(MovieID=x).update(Rating=ave[x])
        # models.Book.objects.filter(id=3).update(title="PHP")
        mo = Movies.objects.get(MovieID=x)
        mo.Rating = ave[x]
        mo.save()


def home(request):
    return render(request, 'mysite/home.html')


def get_top_n_movies(top_n=10):
    """
    根据每个电影的评分获取前top_n的电影的对象
    :param top_n:
    :return: top_n个电影对象
    """
    # 非随机初始化分数
    # init_rating(False)

    movies = Movies.objects.all()
    movie_name = [[]]*len(movies)
    rating = np.zeros((len(movies),))
    search_times = np.zeros((len(movies),))
    like_times = np.zeros((len(movies),))

    sort_arry = []
    for i in range(len(movies)):
        mo = movies[i]
        movie_name[i] = mo.MovieName
        rating[i] = mo.Rating
        like_times[i] = mo.LikeTimes
        search_times[i] = mo.SearchTimes
        sort_arry.append([rating[i],like_times[i],search_times[i],movie_name[i]])

    ind = np.lexsort((-search_times,-like_times,-rating))
    # sort_arry.sort(key= lambda s:(-s[0],-s[1],s[2]))
    result = [movie_name[ind[i]] for i in range(len(ind))]
    return result[:top_n]


def index(request):
    # init_rating()
    # 获取前top_n的电影对象：
    news = Movies.objects.all().order_by('-ProduceYear')
    newslist = news[:8]

    if request.method == "POST":
        request.session['movie_id'] = request.POST['movie_id']
        return redirect('../details', locals())
    else:
        movie_name = get_top_n_movies()
        top_movies = []
        for mn in movie_name:
            top_movies.append(Movies.objects.get(MovieName=mn))

    return render(request, 'mysite/index.html',locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            userid = register_form.cleaned_data['userid']
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            # email = register_form.cleaned_data['email']
            gender = register_form.cleaned_data['gender']
            age = register_form.cleaned_data['age']
            workid = register_form.cleaned_data['workid']
            # print(userid, username, password1, gender, age, workname)
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'mysite/register.html', locals())
            else:
                same_name_user = User.objects.filter(UserID=userid)
                if same_name_user:  # 用户ID唯一
                    message = '用户ID已经存在，请重新选择用户ID！'
                    return render(request, 'mysite/register.html', locals())
                same_name_user = User.objects.filter(UserName=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'mysite/register.html', locals())

                # same_email_user = User.objects.filter(Email=email)
                # if same_email_user:  # 邮箱地址唯一
                #     message = '该邮箱地址已被注册，请使用别的邮箱！'
                #     return render(request, 'mysite/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                # new_user = User.objects.create()
                work_type = WorkType.objects.get(WorkID=workid)
                new_user = User()
                new_user.UserID = userid
                new_user.UserName = username
                new_user.Password = password1
                # new_user.Email = email
                new_user.Gender = gender
                new_user.Age = age
                new_user.WorkID = work_type
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'mysite/register.html', locals())


def logout(request):
    if request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        # return redirect("/index/")
        request.session.flush()
        # 或者使用下面的方法
        # del request.session['is_login']
        # del request.session['user_id']
        # del request.session['user_name']
    return redirect('/index/')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index/')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = '检查填写内容'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            try:
                user = User.objects.get(UserName=username)

                if user.Password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.UserID
                    request.session['user_name'] = user.UserName
                    return redirect('/index/')
                else:
                    message = '密码不正确!'
            except:
                message = '用户不存在!'
        return render(request, 'mysite/login.html', locals())

    login_form = UserForm()
    return render(request, 'mysite/login.html', locals())


def recommend(request):
    username = request.session['user_name']
    user = User.objects.get(UserName=username)
    sl = SearchLogging.objects.all()

    if request.method == "POST":
        request.session['movie_id'] = request.POST['movie_id']
        return redirect('../details', locals())
    cf = UserCf(user.UserID,10,None,None,sl)
    result = cf.top_n_movies
    movielist = []
    for i in result:
        movielist.append(Movies.objects.get(MovieID=i[0]))
    return render(request, 'mysite/recommend.html', locals())


def personal(request):
    username = request.session['user_name']
    user = User.objects.get(UserName=username)
    work_type = WorkType.objects.filter(WorkID=user.WorkID)

    loglist = SearchLogging.objects.filter(UserID=user.UserID)
    collectlist = Collect.objects.filter(UserID=user.UserID)

    if request.method == 'POST':
        request.session['movie_id'] = request.POST['movie_id']
        return redirect('../details', locals())
    else:
        return render(request, 'mysite/personal.html', locals())


def details(request):
    movie = Movies.objects.get(MovieID=request.session['movie_id'])
    typelist = MovieLabel.objects.filter(MovieID=movie.MovieID)
    if not request.session.get('is_login', None):
        return render(request, 'mysite/details.html', locals())

    user = User.objects.get(UserID=request.session['user_id'])
    loglist = SearchLogging.objects.filter(UserID=user, MovieID=movie)
    collectlist = Collect.objects.filter(UserID=user, MovieID=movie)
    log = None
    if len(loglist) == 1:
        log = loglist[0]
    if len(collectlist) == 1:
        collect = "YES"
    else:
        collect = "NO"
    if request.method == "POST":
        like = request.POST['like']
        rate = request.POST['rate']
        collect = request.POST['collect']

        if len(collectlist) == 0:
            if collect == "YES":
                new_collect = Collect()
                new_collect.UserID = user
                new_collect.MovieID = movie
                new_collect.save()
        elif len(collectlist) == 1:
            if collect == "NO":
                Collect.delete(collectlist[0])

        if len(loglist) == 1:
            log = loglist[0]
            log.LikeOrDislike = like
            log.Rating = rate
            log.save()
        else:
            new_searchlogging = SearchLogging()
            new_searchlogging.UserID = user
            new_searchlogging.MovieID = movie
            new_searchlogging.LikeOrDislike = like
            new_searchlogging.Rating = rate
            new_searchlogging.save()
            log = new_searchlogging

    return render(request, 'mysite/details.html', locals())


def search(request):
    if request.method == "POST":
        data_dict = request.POST
        if 'search_name' in data_dict:
            movie_list = Movies.objects.filter(MovieName__icontains=data_dict['search_name'])
        else:
            if 'movie_id' in data_dict:
                request.session['movie_id'] = data_dict['movie_id']
                return redirect('../details', locals())

    return render(request, 'mysite/search.html', locals())


def comedy(request):
    type = MovieType.objects.get(TypeID='5')
    # movie_list = MovieLabel.objects.filter(TypeID=type).order_by('MovieID')
    ind = ['666'+str(i) for i in range(501,571)]
    movie_list = []
    for i in ind:
        movie = MovieLabel.objects.filter(MovieID=i,TypeID=type)
        movie_list += movie

    movie_list = movie_list[:8]

    if request.method == "POST":
        data_dict = request.POST
        if 'movie_id' in data_dict:
            request.session['movie_id'] = data_dict['movie_id']
            return redirect('../details', locals())
    return render(request, 'mysite/comedy.html', locals())


def love(request):
    type = MovieType.objects.get(TypeID='14')
    # movie_list = MovieLabel.objects.filter(TypeID=type).order_by('MovieID')
    ind = ['666'+str(i) for i in range(501,571)]
    movie_list = []
    for i in ind:
        movie = MovieLabel.objects.filter(MovieID=i,TypeID=type)
        movie_list += movie
    movie_list = movie_list[:8]
    if request.method == "POST":
        data_dict = request.POST
        if 'movie_id' in data_dict:
            request.session['movie_id'] = data_dict['movie_id']
            return redirect('../details', locals())
    return render(request, 'mysite/love.html', locals())
