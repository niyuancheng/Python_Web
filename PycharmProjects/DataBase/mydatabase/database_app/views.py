from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .form import *
import datetime
import json
from django.views.decorators.csrf import csrf_exempt
import os
import time
from django.db import connections

from mydatabase import settings


def login(request):
    if request.session.get("is_login", None):
        return redirect('/index/')
    if request.method == "POST":
        message = ""
        login_form = Userform(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = appuser.objects.filter(username=username)
            if user:
                if password != user[0].password:
                    message = "密码不正确"
                else:  # 此时表明用户名和密码都正确
                    request.session['is_login'] = True
                    request.session['user_id'] = user[0].u_id
                    request.session['user_name'] = user[0].username
                    return redirect('/index/', locals())
            else:
                message = "用户名不正确"
        return render(request, 'Login.html', locals())
    login_form = Userform()
    return render(request, 'Login.html', locals())


def homepage(request):
    return render(request, 'homepage.html', locals())


def loginout(request):
    if not request.session.get("is_login"):
        return redirect('/home/')
    request.session.flush()  # 清除用户的会话状态
    return redirect('/index/')


def index(request):
    return render(request, "index.html", locals())


def register(request):
    if request.method == "POST":
        print("已接受请求")
        message = ''
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        password_again = request.POST.get("password_again", None)
        if username and password:
            print("开始处理数据")
            if password_again != password:
                message = "密码不同，请重新输入！！！"
                return render(request, 'register.html', locals())
            else:
                user = appuser.objects.filter(username=username)
                if user:
                    message = "该用户名已存在"
                    return render(request, 'register.html', locals())
                else:
                    test = appuser.objects.all()
                    t = len(test)
                    u = appuser(t + 1, username, password)
                    u.save()
                    return redirect('/login/')
    return render(request, 'register.html', locals())


@csrf_exempt
def Schedule(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        sche = request.POST.get('sche')
        user_id = request.session["user_id"]
        if date and sche:
            sid = len(schedule.objects.all()) + 1
            fmt = '%Y-%m-%d'
            time_tuple = time.strptime(date, fmt)
            year, month, day = time_tuple[:3]
            a_date = datetime.date(year, month, day)
            sche_dule = schedule(sid, sche, a_date)
            sche_dule.save()
            id = len(save_s.objects.all()) + 1
            s = save_s(id, sid, user_id)
            s.save()
            data = {
                "id": sid,
                "schedule": sche,
                "date": a_date.strftime("%Y-%m-%d")
            }
            res = {'data': data}
            return JsonResponse(res)
    elif request.method == 'GET':
        date_off = request.GET.get("date_offset")
        sche = request.GET.get("a_sche")
        record = schedule.objects.filter(s_schedule=sche).update()
    return render(request, 'schedule.html', locals())


@csrf_exempt
def handle(request):
    if request.is_ajax():
        msg = request.POST.get("mes", None)
        print(msg)
        repo = save_s.objects.filter(u_id=request.session['user_id'])
        sche_id = []
        for i in repo:
            sche_id.append(i.s_id)

        data = []
        for i in sche_id:
            item = schedule.objects.filter(s_id=i)[0]
            data.append({
                "id": item.s_id,
                "schedule": item.s_schedule,
                "sdate": item.s_date.strftime('%Y-%m-%d')
            })
        for i in data:
            print(i['schedule'])
        res = {"data": data}
        return JsonResponse(res)


def update_id(request, sid, database):
    with connections[database].cursor() as cursor:
        if database == "database_app_save_s":
            cursor.execute('update table %s set id=id-1 where id > sid', [database])
        elif database == "databse_app_schedule":
            cursor.execute('update table %s set s_id = s_id-1 where s_id>sid', [database])


def delete(request):
    if request.is_ajax():
        pass


@csrf_exempt
def Photo(request):
    message = "无"
    if request.method == "GET":
        message = None
    elif request.method == "POST":
        print("开始处理请求")
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get("image2", None)
        user_id = request.session["user_id"]
        if image1 and image2:
            i1 = photo.objects.filter(img=image1)
            i2 = photo.objects.filter(img=image2)
            if len(i1) != 0 or len(i2) != 0:
                message = "该照片已经重复，故无法再次提交"
                return render(request, 'photo.html', locals())
            else:
                message = "照片保存成功"
                print("已接受到图片")
                l = records.objects.all()
                r = len(l)
                r += 1
                rec = records(r, datetime.datetime.now())
                rec.save()
                img = photo()
                img.r_id = r
                img.img = image1
                img.save()
                print("图片已经保存到本地")
                id = len(save_r.objects.all()) + 1
                s = save_r(id, user_id, r)
                s.save()
                r += 1
                rec = records(r, datetime.datetime.now())
                rec.save()
                img = photo()
                img.r_id = r
                img.img = image2
                img.save()
                id = len(save_r.objects.all()) + 1
                s = save_r(id, user_id, r)
                s.save()
                return redirect('/photo/')
        else:
            print("未接受到图片")
    return render(request, 'photo.html', locals())


def photo_view(request):
    print("开始处理请求")
    message = []
    record = save_r.objects.filter(u_id=request.session['user_id'])
    for i in record:
        if (photo.objects.filter(r_id=i.r_id)):
            image = photo.objects.filter(r_id=i.r_id)[0]
            if image:
                url = str(image.img)
                message.append(url)
    return render(request, 'photo_view.html', locals())


def Usertext(request):
    if request.method == 'POST':
        title = request.POST.get("title", None)
        content = request.POST.get("content", None)
        message = None
        if title and content:
            l = records.objects.all()
            r = len(l)
            r += 1
            rec = records(r, datetime.datetime.now())
            rec.save()
            u = usertext()
            u.r_id = r
            u.title = title
            u.text = content
            u.save()
            user_id = request.session["user_id"]
            id = len(save_r.objects.all()) + 1
            s = save_r(id, user_id, r)
            s.save()
        else:
            message = "日记标题或者内容不可为空"
    if request.method == "GET":
        ori = request.GET.get("original_title", None)
        atitle = request.GET.get("atitle", None)
        acontent = request.GET.get("acontent", None)
        if atitle and acontent:
            usertext.objects.filter(title=ori).update(title=atitle, text=acontent)
    user_id = request.session["user_id"]
    rec = save_r.objects.filter(u_id=user_id)
    diary = []
    for date in rec:
        t = usertext.objects.filter(r_id=date.r_id)
        if t:
            s = records.objects.filter(r_id=date.r_id)
            n = {
                "title": t[0].title,
                "content": t[0].text,
                "time": s[0].r_date_time
            }
            diary.append(n)

    return render(request, 'usertext.html', locals())


def home(request):  # 返回刚进入网站的界面,该界面联系着登录和注册界面还有网站的主页面
    return render(request, "base.html")


@csrf_exempt
def ajax_add(request):
    if request.method == "POST":
        print("开始处理数据")
        text = request.POST.get("text")
        print(text)
        message = {"text": text}
        return JsonResponse(message)
    return render(request, 'test.html', locals())
