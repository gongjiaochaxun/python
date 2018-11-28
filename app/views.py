from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from app.auth import admin_check, login_check
from app.models import *
from datetime import datetime
from app.graph import *
import re


'''
用户管理模块
'''
@admin_check
def user_add(requests):
    username = requests.POST.get('username',None)
    password = requests.POST.get('password',None)
    email = requests.POST.get('email',None)
    sex = requests.POST.get('sex',None)
    role = requests.POST.get('role','user')
    if username and password and email and sex and role:
        tem = User.objects(email=email).first()
        if (tem is None):
            newuser = User(username=username, password=password, email=email, sex=sex, role=role)
            newuser.save()
            return JsonResponse({"data": dict(
                username=username,
                password="************",
                email=email,
                sex=sex,
                role=role,
            ),"res":True}, safe=False)
        else:
            return JsonResponse({"data": "邮箱已注册", "res": False}, safe=False)
    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)


@admin_check
def user_del(requests):
    email = requests.POST.get('email',None)
    if email:
        tem = User.objects(email=email).first()
        if tem:
            tem.delete()
            return JsonResponse({"data":email,"res":True}, safe=False)
        else:
            return JsonResponse({"data": "找不到该用户", "res": False}, safe=False)
    else:
        return JsonResponse({"data":"信息不完整","res":False}, safe=False)


@admin_check
def user_edit(requests):
    username = requests.POST.get('username',None)
    password = requests.POST.get('password',None)
    email = requests.POST.get('email',None)
    sex = requests.POST.get('sex',None)
    role = requests.POST.get('role','user')
    if username and password and email and sex and role:
        tem = User.objects(email=email).first()
        if tem is None:
            return JsonResponse({"data": "找不到该用户", "res": False}, safe=False)
        else:
            tem.username = username
            tem.password = password
            tem.sex = sex
            tem.role = role
            tem.save()
            return JsonResponse({"data": dict(
                username=username,
                password="************",
                email=email,
                sex=sex,
                role=role,
            ),"res":True}, safe=False)
    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)


@admin_check
def user_list(requests):
    users = User.objects()
    ret = [
        {
            "username":_.username,
            "password":_.password,
            "sex":_.sex,
            "role":_.role,
            "email":_.email
        }
        for _ in users]
    return JsonResponse({"data": ret, "res": True}, safe=False)


'''
地点管理模块
'''
@admin_check
def place_add(requests):
    placename = requests.POST.get('placename',None)
    if placename:
        tem = Place.objects(placename=placename).first()
        if tem:
            return JsonResponse({"data":"站点已存在","res":False},safe=False)
        else:
            newplace = Place(placename=placename)
            newplace.save()
            return JsonResponse({"data": placename, "res": True}, safe=False)
    else:
        return JsonResponse({"data":"信息不完整","res":False},safe=False)


@admin_check
def place_del(requests):
    placename = requests.POST.get('placename',None)
    if placename:
        tem = Place.objects(placename=placename).first()
        if not tem:
            return JsonResponse({"data":"站点不存在","res":False},safe=False)
        else:
            tem.delete()
            return JsonResponse({"data": placename, "res": True}, safe=False)
    else:
        return JsonResponse({"data":"信息不完整","res":False},safe=False)


@login_check
def place_list(requests):
    places = Place.objects()
    ret = [
        {
            "placename": _.placename,
            "routes": [__.routename for __ in _.routes]
        }
        for _ in places]
    return JsonResponse({"data": ret, "res": True}, safe=False)

@login_check
def place_list_byroute(requests):
    routename = requests.POST.get('routename', None)
    if routename:
        route = Route.objects(routename=routename).first()
        places = [ _ for _ in route.places]
        ret = [
            {
                "placename": _.placename,
                "routes": [__.routename for __ in _.routes]
            }
            for _ in places]
        return JsonResponse({"data": ret, "res": True}, safe=False)
    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)

@admin_check
def place_edit(requests):
    placename = requests.POST.get('placename',None)
    newplacename = requests.POST.get('newplacename',None)
    if placename and newplacename:
        tem = Place.objects(placename=placename).first()
        if not tem:
            return JsonResponse({"data":"站点不存在","res":False},safe=False)
        else:
            if Place.objects(placename=newplacename).first():
                return JsonResponse({"data": "站点已存在", "res": False}, safe=False)
            else:
                tem.placename = newplacename
                tem.save()
                return JsonResponse({"data": newplacename, "res": True}, safe=False)
    else:
        return JsonResponse({"data":"信息不完整","res":False},safe=False)

@admin_check
def place_del_route(requests):
    placename = requests.POST.get('placename', None)
    routename = requests.POST.get('routename', None)
    if placename and routename:
        place = Place.objects(placename=placename).first()
        route = Route.objects(routename=routename).first()
        if place and route:
            place.del_route(route)
            return JsonResponse({"data": place.placename+" "+route.routename, "res": True}, safe=False)
        else:
            return JsonResponse({"data": "站点或线路不存在", "res": False}, safe=False)
    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)


'''
线路管理模块
'''
@admin_check
def route_add(requests):
    routename = requests.POST.get('routename', None)
    places_str = requests.POST.get('places', None)
    money = requests.POST.get('money', None)
    start_time_str = requests.POST.get('start_time', None)
    stop_time_str = requests.POST.get('stop_time', None)

    if routename and places_str and money and start_time_str and stop_time_str:
        if Route.objects(routename=routename).first():
            return JsonResponse({"data": "线路已存在", "res": False}, safe=False)
        else:
            pattern = re.compile(r'\b\d{2}:\d{2}\b')
            start_time = re.findall(pattern, start_time_str)
            stop_time = re.findall(pattern, stop_time_str)
            if stop_time and start_time:
                places_list = places_str.split(',')
                places = [Place.objects(placename=_).first() for _ in places_list if _ and Place.objects(placename=_).first()]
                newroute = Route(routename=routename, places=places, money=money, start_time=start_time[0], stop_time=stop_time[0])
                newroute.save()
                [_.add_route(newroute) for _ in newroute.places]
                return JsonResponse({"data": routename, "res": True}, safe=False)
            else:
                return JsonResponse({"data": "时间格式错误 HH:MM（24小时制）", "res": True}, safe=False)
    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)

@admin_check
def route_edit(requests):
    routename = requests.POST.get('routename', None)
    places_str = requests.POST.get('places', None)
    money = requests.POST.get('money', None)
    start_time_str = requests.POST.get('start_time', None)
    stop_time_str = requests.POST.get('stop_time', None)

    if routename and places_str and money and start_time_str and stop_time_str:
        newroute = Route.objects(routename=routename).first()
        if not newroute:
            return JsonResponse({"data": "线路不存在", "res": False}, safe=False)
        else:
            pattern = re.compile(r'\b\d{2}:\d{2}\b')
            start_time = re.findall(pattern, start_time_str)
            stop_time = re.findall(pattern, stop_time_str)
            if stop_time and start_time:
                places_list = places_str.split(',')
                places = [Place.objects(placename=_).first() for _ in places_list if _ and Place.objects(placename=_).first()]
                newroute.routename = routename
                newroute.places = places
                newroute.stop_time = stop_time
                newroute.start_time = start_time
                newroute.save()
                [_.add_route(newroute) for _ in newroute.places]
                return JsonResponse({"data": routename, "res": True}, safe=False)
            else:
                return JsonResponse({"data": "时间格式错误 HH:MM（24小时制）", "res": True}, safe=False)
    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)

@admin_check
def route_del(requests):
    routename = requests.POST.get('routename', None)

    if routename:
        print(routename)
        newroute = Route.objects(routename=routename).first()
        if not newroute:
            return JsonResponse({"data": "线路不存在", "res": False}, safe=False)
        else:
            places = newroute.places
            for place in places:
                place.del_route(newroute)
            newroute.delete()
            return JsonResponse({"data": routename, "res": True}, safe=False)

    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)

@admin_check
def route_search(requests):
    routename = requests.POST.get('routename', None)
    if routename:
        routes = Route.objects(routename=routename)
        if not routes:
            return JsonResponse({"data": "线路不存在", "res": False}, safe=False)
        else:
            ret = [
                {
                    "routename": _.routename,
                    "places": [__.placename for __ in _.places if __ ],
                    "start_time": _.start_time,
                    "stop_time": _.stop_time,
                    "money": _.money
                }
                for _ in routes]
            return JsonResponse({"data": ret, "res": True}, safe=False)

    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)

@login_check
def route_list(requests):
    ret = [
        {
            "routename": _.routename,
            "places": [__.placename for __ in _.places if __],
            "start_time": _.start_time,
            "stop_time": _.stop_time,
            "money": _.money
        }
    for _ in Route.objects()]
    return JsonResponse({"data": ret, "res": True}, safe=False)


'''
图表展示模块
'''
@admin_check
def echart_gjw(requests):
    places_str = set([ _.placename for _ in Place.objects() if _.routes and len(_.routes)!=0])
    places =  [{"name":_} for _ in places_str]
    edges_str = set()
    for placelist in [ _.places for _ in Route.objects()]:
        for i in range(0,len(placelist)-1):
            edges_str.add("{s}->{t}".format(s=placelist[i].placename,t=placelist[i+1].placename))
    edges = []
    for i in edges_str:
        tmp = i.split("->")
        edges.append(dict(source=tmp[0],target=tmp[1]))
    ret = {
        "places":places,
        "edges":edges
    }
    return JsonResponse({"data": ret, "res": True}, safe=False)

@admin_check
def echart_zzt(requests):
    ret = [{"placename":_.placename,"value":len(_.routes)} for _ in Place.objects()]
    return JsonResponse({"data": ret, "res": True}, safe=False)

@admin_check
def echart_bzt(requests):
    def dyNow(time: 'str') -> 'bool':
        tmp = time.split(":")
        ntime = datetime.now()
        if ntime.hour<int(tmp[0]):
            return True
        elif ntime.hour>int(tmp[0]):
            return False
        else:
            if ntime.minute<int(tmp[1]):
                return True
            elif ntime.minute>int(tmp[1]):
                return False
            else:
                return False

    allnum = len([ _ for _ in Route.objects()])
    startnum = len([ _ for _ in Route.objects() if dyNow(_.start_time)==False and dyNow(_.stop_time)==True])
    stopnum = len([_ for _ in Route.objects() if dyNow(_.start_time) or dyNow(_.stop_time) == False])

    return JsonResponse({"data": dict(allnum=allnum,startnum=startnum,stopnum=stopnum), "res": True}, safe=False)
'''
线路查询功能
'''
@login_check
def cx(requests):
    s = requests.POST.get('s',None)
    t = requests.POST.get('t',None)
    if s and t:
        ret = Search(s,t)
        if ret:
            return JsonResponse({"data": ret, "res": True}, safe=False)
        else:
            return JsonResponse({"data": "没有相应线路", "res": False}, safe=False)
    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)

'''
用户注册登录模块
'''
def register(requests):
    username = requests.POST.get('username',None)
    password = requests.POST.get('password',None)
    repassword = requests.POST.get('repassword', None)
    email = requests.POST.get('email',None)
    sex = requests.POST.get('sex',None)
    role = requests.POST.get('role','user')
    if username and password and repassword and email and sex and role:
        tem = User.objects(email=email).first()
        if tem is None:
            if password == repassword:
                newuser = User(username=username, password=password, email=email, sex=sex, role=role)
                newuser.save()
                return JsonResponse({"data": dict(
                    username=username,
                    password="************",
                    email=email,
                    sex=sex,
                    role=role,
                ),"res":True}, safe=False)
            else:
                return JsonResponse({"data": "两次密码不一致", "res": False}, safe=False)
        else:
            return JsonResponse({"data": "邮箱已注册", "res": False}, safe=False)
    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)


def login(requests):
    password = requests.POST.get('password',None)
    email = requests.POST.get('email',None)
    if password and email:
        tem = User.objects(password=password, email=email).first()
        if tem:
            requests.session["user_id"] = str(tem.id)
            if tem.role == "admin":
                requests.session["admin_id"] = str(tem.id)
            return JsonResponse({"data": email, "res": True}, safe=False)
        else:
            return JsonResponse({"data": "用户名或密码错误", "res": False}, safe=False)
    else:
        return JsonResponse({"data": "信息不完整", "res": False}, safe=False)

@login_check
def logout(requests):
    try:
        try:
            if requests.session["user_id"]:
                del requests.session["user_id"]
        except:
            pass
        try:
            if requests.session["admin_id"]:
                del requests.session["admin_id"]
        except:
            pass
        return JsonResponse({"data": "退出成功", "res": True}, safe=False)
    except Exception as e:
        return JsonResponse({"data": str(e),"res":False},safe=False)

