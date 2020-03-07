from django.shortcuts import render,redirect
from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment
from django.contrib.contenttypes.models import ContentType
# Create your views here.

def comment(request):
    data = {}
    form=CommentForm(request.POST)
    if form.is_valid():
        if form.cleaned_data["context"].strip():
            model_obj=form.cleaned_data["model_obj"]
            comment_=Comment()
            comment_.content_object=model_obj
            comment_.comment=form.cleaned_data["context"]
            comment_.user=request.user
            reply_id=form.cleaned_data["reply_id"]
            if reply_id<0:
                data["error"]="网页出错"
            elif reply_id==0:
                parent=None
            elif Comment.objects.filter(id=reply_id).exists():
                parent=Comment.objects.get(id=reply_id)
            else:
                data["error"]="评论的对象不存在"
            if not parent is None:
                if not parent.root  is None:
                    comment_.root=parent.root
                else:
                    comment_.root=parent
                comment_.parent=parent
                comment_.reply_to=parent.user
            if not parent is None:
                data['reply_to']=comment_.reply_to.username
                data['root_id'] = comment_.root.id if not comment_.root.id is None else ''
            else:
                data["reply_to"]=''
            comment_.save()
    data["user"]=request.user.username
    data["time"]=comment_.comment_time.strftime("%Y-%m-%d %H:%I:%S" )
    data["content"]=comment_.comment
    data["id"]=comment_.id
    # referer = request.META.get("HTTP_REFERER", "/")获取当前页的网址
    return  JsonResponse(data)