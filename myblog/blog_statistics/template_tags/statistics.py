from django import template
from ..models import BlogReadNum,Comment,LikeRecord,LikeNum
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog

register=template.Library()

@register.simple_tag()
def get_read_num(id):
    model=ContentType.objects.get_for_model(Blog)
    if BlogReadNum.objects.filter(content_type=model,object_id=id).exists():
        count=BlogReadNum.objects.get(content_type=model,object_id=id)
        return count.read_num
    else:
        return 0
@register.simple_tag()
def get_comment_num(id,obj):
    model=ContentType.objects.get_for_model(obj)
    if Comment.objects.filter(content_type=model,object_id=id).exists():
        count=Comment.objects.filter(content_type=model,object_id=id).count()
        return count
    else:
        return 0
@register.simple_tag(takes_context=True)
def get_like_status(context,obj,id):
    model=ContentType.objects.get_for_model(obj)
    user =context["user"]
    if LikeRecord.objects.filter(content_type=model,object_id=id,user=user).exists():
        return "active"
    else:
        return ""

@register.simple_tag()
def get_like_num(obj,id):
    model=ContentType.objects.get_for_model(obj)
    if LikeNum.objects.filter(content_type=model,object_id=id).exists():
        num=LikeNum.objects.get(content_type=model,object_id=id)
        return num.like_num
    else:
        return 0