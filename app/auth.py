from django.http import JsonResponse
from app.models import User


def login_check(func):
    def wrapper(request,*args,**kwargs):
        #return func(request, *args, **kwargs)
        if not request.session.get("user_id", None):
            return JsonResponse({"data":"您未登录系统","res":False}, safe=False)
        return func(request,*args, **kwargs)
    return wrapper


def admin_check(func):
    def wrapper(request,*args,**kwargs):
        #return func(request, *args, **kwargs)
        if not request.session.get("user_id", None):
            return JsonResponse({"data":"您未登录系统","res":False}, safe=False)
        tem = User.objects(id=request.session.get("user_id", None), role="admin").first()
        if not tem:
            return JsonResponse({"data": "您没有权限", "res": False}, safe=False)
        return  func(request,*args, **kwargs)
    return wrapper