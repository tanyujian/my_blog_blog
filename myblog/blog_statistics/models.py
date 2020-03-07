from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from myuser.models import MyUser
# Create your models here.

class BlogReadNum(models.Model):
    read_num=models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)#获取与主键的关系
    object_id = models.PositiveIntegerField()#获取关联那个莫模型的id
    content_object = GenericForeignKey('content_type', 'object_id')#相关连形成主键
    class Meta:
        verbose_name_plural = "ReadNum"

class BlogRank(models.Model):
    read_num=models.IntegerField(default=0)
    blog_time=models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 获取与主键的关系
    object_id = models.PositiveIntegerField()#获取关联那个莫模型的id
    content_object = GenericForeignKey('content_type', 'object_id')#相关连形成主键
    class Meta:
        verbose_name_plural = "BlogRank"

class Comment(models.Model):
    comment=RichTextUploadingField()
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    comment_time=models.DateTimeField(auto_now_add=True)
    reply_to=models.ForeignKey(MyUser,related_name="replies",on_delete=models.CASCADE,null=True)
    root=models.ForeignKey("self",related_name="root_comment",null=True,blank=True,on_delete=models.CASCADE)
    parent = models.ForeignKey("self", related_name="parent_comment", null=True,blank=True, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 获取与主键的关系
    object_id = models.PositiveIntegerField()#获取关联那个莫模型的id
    content_object = GenericForeignKey('content_type', 'object_id')#相关连形成主键
    class Meta:
        ordering=["comment_time"]
        verbose_name_plural="comment"
    def __str__(self):
        return self.comment