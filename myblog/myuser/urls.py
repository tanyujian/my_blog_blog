from django.contrib.auth.urls import path
from . import views

urlpatterns=[
    path("login/",views.log_in,name="login"),
    path("logout/",views.log_out,name="logout"),
    path("signup/",views.sign_up,name="signup"),
    path("send",views.send_email,name="send_email"),
    path("personal",views.personal,name="personal"),
    path("change_nickname",views.change_nickname,name="change_nickname"),
    path("change_email",views.change_email,name="change_email")
]