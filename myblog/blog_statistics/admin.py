from django.contrib import admin
from .models import BlogRank,BlogReadNum,Comment,LikeRecord,LikeNum
# Register your models here.

class BlogReadNumAdmin(admin.ModelAdmin):
    list_display = ["id","read_num"]

class BlogRankAdmin(admin.ModelAdmin):
    list_display = ["id","read_num","blog_time"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id","user"]

class LikeNumAdmin(admin.ModelAdmin):
    list_display = ["id","like_num"]
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ["id","user","like_time"]

admin.site.register(BlogReadNum,BlogReadNumAdmin)
admin.site.register(BlogRank,BlogRankAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(LikeNum,LikeNumAdmin)
admin.site.register(LikeRecord,LikeRecordAdmin)