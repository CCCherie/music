from django.shortcuts import render,redirect
from index.models import *
from user.models import *
from django.db.models import Q
from django.contrib.auth import login,logout
from django.contrib.auth.hashers import check_password
from .form import MyUserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

@login_required(login_url='/user/login.html')
def homeView(request,page):
    # 用户的注册和登陆
    search_song = Dynamic.objects.select_related('song').order_by('-dynamic_search').all()[:4]
    # 分页功能
    song_info = request.session.get('play_list',[])
    paginator = Paginator(song_info,3)
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request,'home.html',locals())


# 用户注册和登录
def loginView(request):
    # 表单对象user
    user = MyUserCreationForm()
    # 表单提交
    if request.method == 'POST':
        # 判断表单提交是用户登录还是用户注册
        # 用户登录
        if request.POST.get('loginUser',''):
            loginUser = request.POST.get('loginUser','')
            password = request.POST.get('password','')
            if MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)):
                user = MyUser.objects.filter(Q(mobile=loginUser) | Q(username=loginUser)).first()
                if check_password(password,user.password):
                    login(request,user)
                    return redirect('/user/home/1.html')
                else:
                    tips = '密码错误'
            else:
                tips = '用户不存在'
        # 用户注册
        else:
            user = MyUserCreationForm(request.POST)
            if user.is_valid():
                user.save()
                tips = '注册成功'
            else:
                if user.errors.get('username',''):
                    user.save()
                    tips = '注册成功'
                else:
                    if user.errors.get('username',''):
                        tips = user.errors.get('username','注册失败')
                    else:
                        tips = user.errors.get('mobile','注册失败')
    return render(request,'login.html',locals())        


# 退出登陆
def logoutView(request):
    logout(request)
    return redirect('/')