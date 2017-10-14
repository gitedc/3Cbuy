from django.shortcuts import render,redirect
from django.http import HttpResponseNotAllowed,JsonResponse,HttpResponse
# import sys
# import os
# sys.path.append(os.path.join(sys.path[0], "df_order"))
from df_order.models import BaseModelManager as c
from df_order.models import BaseModel
# from df_order.views import *
# print([x for x in dir() if not x.start0swith("_")])
# print(dir(df_order.models))
from df_user.models import Passport,PassportManager,Address,AddressManager,BrowseHistory,BrowseHistoryManager
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST,require_GET,require_http_methods
from utils.get_hash import get_hash
from datetime import datetime,timedelta
# from dailyfresh import settings
from utils.decorators import login_required
from df_order.models import OrderBasic

'''
def require_POST(view_func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'POST':
            return redirect('/user/register/')
        else :
            return view_func
    return wrapper
'''

# @require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')

        Passport.objects.add_one_passport(username=username, password=get_hash(password), email=email)
        msg = '<h1>欢迎您成为dailyfresh会员</h1>'
        send_mail('欢迎信息',msg,settings.EMAIL_FROM, [email, ],)

        return redirect('/')
# @require_POST
# def register_handle(request):
#     username = request.POST.get('username')
#     password = request.POST.get('pwd')
#     email = request.POST.get('email')
def login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    passport = Passport.objects.get_one_passport(username=username, password=password)
    if passport:
        next = request.session.get('pre_url_path','/')
        jres = JsonResponse({'res': 1,'next':next})
        remember = request.POST.get('remember')
        if remember == 'true':
            jres.set_cookie('username', username, expires=datetime.now()+timedelta(days=14))
        request.session['is_login']=True
        request.session['passport_id']=passport.id
        request.session['username'] = username
        return jres
    else:
        return JsonResponse({'res': 0})

def logout(request):
    request.session.flush()
    return redirect('/user/login/')

def login(request):
    if 'username' in request.COOKIES:
        username = request.COOKIES['username']
    else:
        username = ''
    return render(request, 'login.html', {'usernam':username})


def register_check(request):
    username = request.GET.get('username')
    p = Passport.objects.get_one_passport(username=username)
    if p:
        return JsonResponse({'res': 0})
    else:
        return JsonResponse({'res': 1})

@require_http_methods(['GET','POST'])
@login_required
def address(request):
    passport_id = request.session['passport_id']
    if request.method == 'GET':
        addr = Address.objects.get_default_address(passport_id = passport_id)
    else:
        receive_name = request.POST.get('uname')
        receive_addr = request.POST.get('addr')
        receive_phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        addr =  Address.objects.add_one_address(passport_id=passport_id,receive_name = receive_name,receive_phone = receive_phone,receive_addr=receive_addr,zip_code = zip_code)

        addr = Address.objects.get_default_address(passport_id=passport_id)
    return render(request, 'user_center_site.html',{'addr':addr,'page':'addr'})

@login_required
def usercenter(request):
    passport_id = request.session['passport_id']
    addr = Address.objects.get_default_address(passport_id=passport_id)
    bro_list = BrowseHistory.objects_logic.get_browse_list_by_passport(passport_id=passport_id)



    return render(request, 'user_center_info.html', {'addr':addr, 'page': 'user', 'bro_list':bro_list})
#
@login_required
def order(request):
    passport_id = request.session.get('passport_id')
    order_basic_list = OrderBasic.objects_logic.get_order_basic_list_by_passport(passport_id=passport_id)


    return render(request,'user_center_order.html',{'page':'order','order_basic_list':order_basic_list})



def test1(request):

    return render(request, 'base_no_cart_count.html')

def test2(request):
    return render(request, 'base.html')


# Create your views here.
