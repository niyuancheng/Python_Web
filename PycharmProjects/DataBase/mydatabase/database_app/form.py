from django import forms
from captcha.fields import CaptchaField
class Userform(forms.Form):
    username = forms.CharField(max_length=30,label="用户名",widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=30,label="密码", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')

class Registerform(forms.Form):
    gender = (
        ('male','男'),
        ('female','女')
    )
    username = forms.CharField(max_length=30,label="你的用户名",widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=30,label="密码",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_again = forms.CharField(max_length=30,label="确认密码",widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label='性别', choices=gender)
    captcha = CaptchaField(label='验证码')

