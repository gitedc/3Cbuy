from django.shortcuts import render
from utils.decorators import login_required
from df_cart.models import Cart
from df_goods.models import Goods
from django.http import JsonResponse
from django.views.decorators.http import require_GET,require_POST,require_http_methods

@require_GET
@login_required
def cart_add(request):
    passport_id = request.session.get('passport_id')
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')

    goods = Goods.objects.get_goods_by_id(goods_id=goods_id)
    if goods.goods_stock < int(goods_count):
        return JsonResponse({'res': 0})
    else:
        Cart.objects.add_one_cart(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
        return JsonResponse({'res': 1})


@require_GET
@login_required
def cart_count(request):
    passport_id = request.session.get('passport_id')
    res = Cart.objects.get_cart_count_by_passport(passport_id=passport_id)

    return JsonResponse({'res':res})

@login_required
def cart_show(request):
    passport_id = request.session.get('passport_id')
    cart_list = Cart.objects_logic.get_cart_list_by_passport(passport_id=passport_id)
    return render(request, 'cart.html', {'cart_list':cart_list})
# Create your views here.

@require_GET
@login_required
def cart_update(request):
    goods_id = request.GET.get('goods_id')
    goods_count = request.GET.get('goods_count')
    passport_id = request.session.get('passport_id')
    update_res = Cart.objects.update_cart_info_by_passport(passport_id=passport_id,goods_id=goods_id,goods_count=int(goods_count))

    if update_res:
        return JsonResponse({'res':1})
    else:
        return JsonResponse({'res':0})

def cart_del(request):
    cart_id = request.GET.get('cart_id')

    try:
        cart_info = Cart.objects.get_one_cart_by_cartid(cart_id=cart_id)
        cart_info.delete()
        return JsonResponse({'res':1})
    except:
        return JsonResponse({'res':0})








