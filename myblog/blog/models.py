from django.db import models
from myuser.models import MyUser
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
#博客类型数据表
class BlogType(models.Model):
    blog_type=models.CharField(max_length=50)
    class Meta:
        verbose_name_plural="blog_type"
    def __str__(self):
        return self.blog_type

#博客数据表
class Blog(models.Model):
    nature=models.ForeignKey(BlogType,on_delete=models.CASCADE)
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    title=models.CharField(max_length=30)
    content=RichTextUploadingField()
    blog_date=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural="myblog"
        ordering=["-blog_date"]

