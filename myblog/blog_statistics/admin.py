from django.contrib import admin
from .models import BlogRank,BlogReadNum,Comment
# Register your models here.

class BlogReadNumAdmin(admin.ModelAdmin):
    list_display = ["id","read_num"]

class BlogRankAdmin(admin.ModelAdmin):
    list_display = ["id","read_num","blog_time"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id","user"]

admin.site.register(BlogReadNum,BlogReadNumAdmin)
admin.site.register(BlogRank,BlogRankAdmin)
admin.site.register(Comment,CommentAdmin)