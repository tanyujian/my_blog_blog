import random,string
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,get_user_model,authenticate
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import LoginForm,SignupForm,ChangeNickname,ChangeEmail
from django.urls import reverse
# Create your views here.
#登陆
def log_in (request):
    content = {}
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            user=form.cleaned_data["user"]
            login(request,user)
            return redirect('main')
    else:
        form=LoginForm()
    content["title"]="登陆"
    content["send"]=""
    content["nature"]="hidden"
    content["forms"]=form
    return render(request,'user_forms',content)

def log_out(request):
    logout(request)
    return redirect('main')
#注册
def sign_up(request):
    content = {}
    if request.method=="POST":
        form=SignupForm(request.POST,request=request)
        if form.is_valid():
            form.save()
            user=authenticate(username=form.cleaned_data["username"],password=form.cleaned_data["password1"])
            user.email=form.cleaned_data["email"]
            user.nickname=form.cleaned_data["nickname"]
            login(request,user)
            del request.session["code"]
            return redirect("main")

    else:
        form=SignupForm()
    content["title"]="注册"
    content["send"]="发送验证码"
    content["nature"]=""
    content["forms"]=form
    return render(request,'user_forms',content)
#发送邮件
def send_email(request):
    data={}
    email=request.GET.get("email")
    User=get_user_model()
    if User.objects.filter(email=email).exists():
        data["success"]="此邮箱已存在"
        return JsonResponse(data)
    code=''.join(random.sample(string.digits+string.ascii_letters,6))
    request.session["code"]=code
    send_mail(
        '邮箱验证',
        '验证码：%s' %code,
        '1277466401@qq.com',
        [email],
        fail_silently=False,
    )
    data["success"]="发送成功"
    return JsonResponse(data)
#个人资料
def personal(request):
    return render(request,"personal.html")
#改变昵称
def change_nickname(request):
    content={}
    if request.method=="POST":
        form=ChangeNickname(request.POST)
        previous = request.GET.get("from",reverse("main"))
        if form.is_valid():
            User=get_user_model()
            user=User.objects.get(username=request.user.username)
            user.nickname=form.cleaned_data["nickname"]
            user.save()
            return redirect(previous)
    else:
        form=ChangeNickname()
    content["title"]="修改昵称"
    content["send"]=""
    content["nature"]="hidden"
    content["forms"]=form
    return render(request,'user_forms',content)
#改变邮箱
def change_email(request):
    content = {}
    if request.method=="POST":
        form=ChangeEmail(request.POST,request=request)
        if form.is_valid():
            User=get_user_model()
            user=User.objects.get(username=request.user.username)
            user.email=form.cleaned_data["email"]
            user.save()
            return redirect("main")
    else:
        form=ChangeEmail()
    content["title"]="修改"
    content["send"]="发送验证码"
    content["nature"]=""
    content["forms"]=form
    return render(request,'user_forms',content)