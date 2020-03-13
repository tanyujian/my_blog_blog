from django.shortcuts import render,redirect
from django.http import JsonResponse
from .forms import CommentForm
from .models import Comment,LikeRecord,LikeNum
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
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

def like(request):
    data={}
    is_like=request.GET.get("is_like")
    model=request.GET.get("model")
    id=request.GET.get("id")
    try:
        get_model = ContentType.objects.get(model=model)
        if not request.user.is_authenticated:
            return JsonResponse({"error":"请登录"})
    except ObjectDoesNotExist:
        return JsonResponse({"error":"没有此博客"})

    if is_like=="true":
        likes,create=LikeRecord.objects.get_or_create(content_type=get_model,object_id=id,user=request.user)
        if create:
            like_=LikeNum.objects.get_or_create(content_type=get_model,object_id=id)
            like_[0].like_num +=1
            like_[0].save()
            data["success"]="success"
            data["like_num"]=like_[0].like_num

        else:
            data["error"]="你已点赞"
    else:
        if LikeRecord.objects.filter(content_type=get_model,object_id=id,user=request.user).exists():
            like_record=LikeRecord.objects.get(content_type=get_model,object_id=id,user=request.user)
            like_record.delete()
            like_,create=LikeNum.objects.get_or_create(content_type=get_model,object_id=id)
            if not create:
                like_.like_num -=1
                like_.save()
                data["like_num"]=like_.like_num
                data["success"]="取消点赞"
            else:
                data["error"]="取消失败"
        else:
            data["error"]="不存在此纪录"
    return JsonResponse(data)

