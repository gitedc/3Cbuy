from django.db import models
from db.base_model import BaseModel
from db.base_manage import BaseModelManager
from django.db.models import Sum
from df_goods.models import Image

class CartLogicManage(BaseModelManager):
    def get_cart_list_by_passport(self,passport_id):
        cart_list = Cart.objects.get_cart_list_by_passport(passport_id=passport_id)
        for cart in cart_list:
            img = Image.objects.get_image_by_goods_id(goods_id=cart.goods.id)
            cart.img_url = img.img_url
        return cart_list

    def get_cart_list_by_id_list(self,cart_id_list):
        cart_list = Cart.objects.get_cart_list_by_id_list(cart_id_list=cart_id_list)
        for cart in cart_list:
            img = Image.objects.get_image_by_goods_id(goods_id=cart.goods.id)
            cart.img_url = img.img_url
        return cart_list


class CartManage(BaseModelManager):
    def get_one_cart_by_cartid(self,cart_id):
        cart = self.get_one_object(id=cart_id)
        return cart

    def get_one_cart(self, goods_id, passport_id):
        cart = self.get_one_object(goods_id=goods_id, passport_id=passport_id)
        return cart

    def add_one_cart(self, goods_id, goods_count, passport_id):
        cart = self.get_one_cart(goods_id=goods_id, passport_id=passport_id)
        if cart:
            cart.goods_count += int(goods_count)
            cart.save()
        else:
            cart = self.create_one_object(goods_id=goods_id,goods_count=goods_count,passport_id=passport_id)
        return cart
    def get_cart_count_by_passport(self, passport_id):
        res_dict =  self.get_object_list(filters={'passport_id':passport_id}).aggregate(Sum('goods_count'))
        res = res_dict['goods_count__sum']
        if res is None:
            res = 0
        return res
    def get_cart_list_by_passport(self, passport_id):
        cart_list = self.get_object_list(filters={'passport_id':passport_id})
        return cart_list

    def update_cart_info_by_passport(self, passport_id, goods_id, goods_count):
        cart =  self.get_one_cart(passport_id=passport_id, goods_id=goods_id)
        if cart:
            if cart.goods.goods_stock < goods_count:
                return False
            else:
                cart.goods_count = goods_count
                cart.save()
                return True
        else:
            self.add_one_cart(passport_id=passport_id, goods_id=goods_id, goods_count=goods_count)
            return False

    def get_cart_list_by_id_list(self,cart_id_list):
        cart_list = self.get_object_list(filters={'id__in':cart_id_list})
        return cart_list

    def get_goods_count_and_amout_by_id_list(self, cart_id_list):
        total_count,total_price = 0,0
        cart_list = self.get_object_list(filters={'id__in':cart_id_list})
        for cart in cart_list:
            total_count += cart.goods_count
            total_price += cart.goods.goods_price
        return total_count,total_price

class Cart(BaseModel):

    passport = models.ForeignKey('df_user.Passport',verbose_name='账户')
    goods = models.ForeignKey('df_goods.Goods',verbose_name='商品')
    goods_count = models.IntegerField(default=1,verbose_name='商品数目')

    objects = CartManage()
    objects_logic = CartLogicManage()
    class Meta:
        db_table = 's_cart'







# Create your models here.
