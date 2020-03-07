from django.contrib import admin
from .models import BlogType,Blog
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ["title","user","blog_date"]

class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ["id","blog_type",]

admin.site.register(Blog,BlogAdmin)
admin.site.register(BlogType,BlogTypeAdmin)