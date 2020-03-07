from django import template
from ..models import Blog


register=template.Library()#注册模板标签
@register.simple_tag()
def get_blog_count(obj):
    count=Blog.objects.filter(nature=obj).count()
    return count
