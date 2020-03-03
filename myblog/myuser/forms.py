from django import forms
from django.contrib.auth import get_user_model,authenticate

class LoginForm(forms.Form):
    username= forms.CharField(label='用户名',
                              widget=forms.TextInput(attrs={'class':"form_control","placeholder":"输入你的用户名"}))
    password=forms.CharField(label="密码",
                             widget=forms.PasswordInput(attrs={"class":"forms_control","placeholder":"输入密码"}))
    def clean(self):
        username=self.cleaned_data['username']
        password=self.cleaned_data['password']
        user= authenticate(username=username,password=password)
        if user is None:
            raise forms.ValidationError("用户名或密码错误")
        return self.cleaned_data