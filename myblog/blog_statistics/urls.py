from django.contrib.auth.urls import path
from .import views
urlpatterns=[
    path("",views.comment,name="comment")
]