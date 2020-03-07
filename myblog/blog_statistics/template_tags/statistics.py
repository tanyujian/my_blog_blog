from django import template
from ..models import BlogReadNum,Comment
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