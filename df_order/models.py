from django.db import models
from df_user.models import Passport,Address
from db.base_manage import BaseModelManager
from db.base_model import BaseModel
from df_goods.models import Image

class OrderBasicLogicManager(BaseModelManager):
    def get_order_basic_list_by_passport(self,passport_id):
        order_basic_list = OrderBasic.objects.get_order_basic_list_by_passport(passport_id=passport_id)
        for order_basic in order_basic_list:
            order_detail_list = OrderDetail.objects_logic.get_oder_detail_list_by_order_id(order_id = order_basic.order_id)
            order_basic.order_detail_list = order_detail_list
        return order_basic_list

class OrderBasicManager(BaseModelManager):

    def add_one_order_basic_info(self,order_id,passport_id,addr_id,total_count,
                                 total_price,transit_price,pay_method):
        order_basic = self.create_one_object(order_id=order_id,passport_id=passport_id, addr_id=addr_id,
                                             total_count=total_count,total_price=total_price,
                                             transit_price=transit_price,pay_method=pay_method)
        print('ok')
        return order_basic
    def get_order_basic_list_by_passport(self,passport_id):
        order_basic_list = self.get_object_list(filters={'passport_id':passport_id})
        return order_basic_list

class OrderBasic(BaseModel):
    order_id = models.CharField(max_length=64,primary_key=True,verbose_name='订单id')
    passport = models.ForeignKey('df_user.Passport',verbose_name='用户')
    addr = models.ForeignKey('df_user.Address',verbose_name='收件地址')
    total_count = models.IntegerField(default=1,verbose_name="商品总数")
    total_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="商品总价")
    transit_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品运费')
    pay_method = models.IntegerField(default=1,verbose_name='付款方式')
    order_status = models.IntegerField(default=1,verbose_name='交易状态')

    objects = OrderBasicManager()
    objects_logic = OrderBasicLogicManager()
    class Meta:
        db_table = 's_order_basic'

class OrderDetailLogicManager(BaseModelManager):
    def get_oder_detail_list_by_order_id(self,order_id):
        order_detail_list = OrderDetail.objects.get_order_detail_list_by_order_id(order_id=order_id)
        for order_detail in order_detail_list:
            image = Image.objects.get_image_by_goods_id(goods_id=order_detail.goods.id)
            order_detail.goods.img_url = image.img_url
        return order_detail_list

class OrderDetailManager(BaseModelManager):
    def add_one_order_detail_info(self,order_id,goods_id,goods_count,goods_price):
        order_detail = self.create_one_object(order_id=order_id,goods_id=goods_id,
                                              goods_count=goods_count,goods_price=goods_price)
        return order_detail

    def get_order_detail_list_by_order_id(self,order_id):
        order_detail_list = self.get_object_list(filters={'order_id':order_id})
        return order_detail_list


class OrderDetail(BaseModel):
    order = models.ForeignKey('OrderBasic',verbose_name='基本订单')
    goods = models.ForeignKey('df_goods.Goods',verbose_name='商品')
    goods_count = models.IntegerField(default=1,verbose_name='商品数量')
    goods_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品价格')
    objects= OrderDetailManager()
    objects_logic = OrderDetailLogicManager()

    class Meta:
        db_table = 's_order_detail'


# Create your models here.
