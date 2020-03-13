from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import   Q
from .forms import ChangeBlog
from .models import BlogType,Blog
from .until import get_classify
from blog_statistics.models import BlogRank,BlogReadNum
from blog_statistics.forms import CommentForm
from blog_statistics.models import Comment

# Create your views here.

@login_required(login_url="login")
def send_blog(request):
    content={}
    if request.method=="POST":
        form =ChangeBlog(request.POST)
        if form.is_valid():
            blog_=form.cleaned_data["blog_type"]
            blog_type=BlogType.objects.get(blog_type=blog_)
            blog=Blog()
            blog.user=request.user
            blog.content=form.cleaned_data["content"]
            blog.title=form.cleaned_data["title"]
            blog.nature=blog_type
            blog.save()
            return redirect("main")            
    else:
        form=ChangeBlog()
    content["forms"]=form
    content["title"]="发送博客"
    content["send"]=""
    content["nature"]="hidden"
    return render(request,"send_blog.html",content)

#博客主页
def blog_main(request):
    blog_data = Blog.objects.all()
    content=get_classify(request,blog_data)
    
    return render(request,"blog_main.html",content)

def  classify_type(request,id):
    blog_type=BlogType.objects.get(id=id)
    blog_data=Blog.objects.filter(nature=blog_type)
    content = get_classify(request,blog_data)
    return render(request, "blog_main.html", content)
def classify_date(request,year,month):
    blog_data=Blog.objects.filter(blog_date__year=year,blog_date__month=month)
    content = get_classify(request,blog_data)
    return render(request, "blog_main.html", content)
def blog_detail(request,id):
    content={}
    model = ContentType.objects.get_for_model(Blog)
    if not request.COOKIES.get("blog_%s"%id):

        #增加阅读数
        blog_read,create=BlogReadNum.objects.get_or_create(content_type=model,object_id=id)
        blog_read.read_num+=1
        blog_read.save()
        date=timezone.now().date()
        #增加排名
        blog_rank,create=BlogRank.objects.get_or_create(content_type=model,object_id=id,blog_time=date)
        blog_rank.read_num+=1
        blog_rank.save()

    #获取评论
    comment=Comment.objects.filter(content_type=model,object_id=id,parent=None).order_by("-comment_time")
    comment_form=CommentForm(initial={"object_id":id,"content_type":model,"reply_id":"0"})
    content["comment"]=comment
    content["comment_form"]=comment_form
    #对博客添加上一篇下一篇
    blog=get_object_or_404(Blog,id=id)
    blog_previous=Blog.objects.filter(id__gt=id).last()
    blog_next=Blog.objects.filter(id__lt=id).first()
    content["blog_next"]=blog_next
    content["blog_previous"]=blog_previous
    content["blog"]=blog
    response= render(request,"blog_detail.html",content)
    #添加cookies来判断阅读数
    response.set_cookie("blog_%s"%id,"true")
    return response

def search(request):
    code=request.GET.get("search",'').strip()
    code_=code.split(" ")
    contain=None
    for i in code_:
        if contain is None:
            contain=Q(title__icontains=i)
        else:
            contain=contain|Q(title__contains=i)
    blog_data=Blog.objects.filter(contain)
    content=get_classify(request,blog_data)
    return render(request,"blog_main.html",content)

def add(request):
    user=request.user
    types=get_object_or_404(BlogType,id=2)
    for i in range(0,30):
        blog=Blog()
        blog.title="Django学习改良版本 %s" %i
        blog.content="xxxxxxxxxxx %s" %i
        blog.user=user
        blog.nature=types
        blog.save()
    return redirect("main")

