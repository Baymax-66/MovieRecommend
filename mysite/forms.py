from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.Form):

    work=(( 0,  "other")
     , ( 1,"academic/educator")
     , ( 2,"artist")
     , ( 3,"clerical/admin")
     , ( 4,"college/grad student")
     , ( 5,"customer service")
     , ( 6,"doctor/health care")
     , ( 7,"executive/managerial")
     , ( 8,"farmer")
     , ( 9,"homemaker")
     , (10,"K-12 student")
     , (11,"lawyer")
     , (12,"programmer")
     , (13,"retired")
     , (14,"sales/marketing")
     , (15,"scientist")
     , (16,"self-employed")
     , (17,"technician/engineer")
     , (18,"tradesman/craftsman")
     , (19,"unemployed")
     , (20,"writer"),)
    sex = (
        ("M", "男"),
        ("F", "女")
    )

    userid = forms.CharField(label="用户ID", max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='性别', choices=sex)
    age = forms.CharField(label="年龄", widget=forms.TextInput(attrs={'class': 'form-control'}))
    workid = forms.ChoiceField(label="工作ID", choices=work)


"""
    功能：展示该电影的主要信息
动作：有个表单（用来评分，加上是否喜欢，收藏按钮）
数据库：将浏览记录插入数据库，并且将结果展示出来。
"""


class DetailsForm(forms.Form):
    favor = (
                ('YES', '喜欢'),
                ("NO", "不喜欢"),
             )
    mark = (
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
            )
    collect = (
        ("YES", "是"),
        ("NO", "否"),
    )
    # like = forms.ChoiceField(label="是否喜欢：", choices=favor)
    collector = forms.ChoiceField(label="是否收藏：", choices=collect)
    rate = forms.ChoiceField(label="评分：", choices=mark)
