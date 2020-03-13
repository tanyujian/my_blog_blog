from django.contrib.auth.urls import path
from . import views
urlpatterns=[
    path("send_blog/",views.send_blog,name="send_blog"),
    path("blog_main/",views.blog_main,name="blog_main"),
    path("type_class<id>/",views.classify_type,name="class_type"),
    path("date_class<year><month>/",views.classify_date,name="class_date"),
    path("blog<id>/",views.blog_detail,name="blog_detail"),
    path("search/",views.search,name="search")

]