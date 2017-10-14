from django.shortcuts import render
from django.views.decorators.http import require_GET,require_POST,require_http_methods
from django.db import transaction
from df_order.models import OrderDetail, OrderBasic
from utils.decorators import login_required
from django.http import JsonResponse
from df_user.models import Address
from df_cart.models import Cart
from datetime import datetime
# from .models import OrderBasic,OrderDetail


# Create your views here.
def order_place(request):
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)
    cart_id_list = request.POST.getlist('cart_id')
    cart_list = Cart.objects_logic.get_cart_list_by_id_list(cart_id_list=cart_id_list)
    cart_id_list = ','.join(cart_id_list)
    print("order_place")

    return render(request, 'place_order.html', {'addr':addr,'cart_list':cart_list,
                                              'cart_id_list':cart_id_list})

# def order_commit(request):
#     print("done")
#     return JsonResponse({'res': 0})

@require_POST
@login_required
@transaction.atomic
def order_commit(request):
    print('111111111')
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    cart_id_list = request.POST.get('cart_id_list')
    passport_id = request.session.get('passport_id')
    order_id = datetime.now().strftime('%Y%m%d%H%M%S')+str(passport_id)
    transit_price = 10.0
    cart_id_list = cart_id_list.split(',')
    total_count,total_price = Cart.objects.get_goods_count_and_amout_by_id_list(cart_id_list=cart_id_list)
    save_id = transaction.savepoint()
    try:
        print('11')
        OrderBasic.objects.add_one_order_basic_info(order_id=order_id, passport_id=passport_id,
                                                    addr_id=addr_id, transit_price=transit_price,
                                                    pay_method=pay_method, total_count=total_count,
                                                    total_price=total_price)
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        for cart in cart_list:
            if cart.goods_count < cart.goods.goods_stock:
                goods_id = cart.goods.id
                goods_count = cart.goods_count
                goods_price = cart.goods.goods_price
                OrderDetail.objects.add_one_order_detail_info(order_id=order_id,
                                            goods_id=goods_id, goods_count=goods_count,
                                                              goods_price=goods_price)
                print(1111)
                cart.goods.goods_stock -= cart.goods_count
                cart.goods.goods_sales += cart.goods_count
                cart.goods.save()
                cart.delete()
            else:
                transaction.savepoint_rollback(save_id)
                return JsonResponse({'res': 0, 'content': '库存不足'})
    except Exception as e:
        transaction.savepoint_rollback(save_id)
        return JsonResponse({'res':0, 'content': '服务器错误'})
    transaction.savepoint_commit(save_id)
    return JsonResponse({'res': 1, 'content': '测试一下'})




