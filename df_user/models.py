from django.db import models
from db.base_model import BaseModel
from db.base_manage import BaseModelManager
from utils.get_hash import get_hash
from df_goods.models import Goods,Image


# from utils import get_hash
class PassportManager(BaseModelManager):

    def add_on_passport1(self, username,password,email):

        model_class = self.model
        passport = model_class()
        passport.username = username
        passport.password = get_hash(password)
        passport.email = email
        passport.save()
        return passport

    def add_one_passport(self,username,password,email):
        passport = self.create_one_object(username = username,password = get_hash(password),email = email)
        return passport

    def get_one_passport(self,username,password=None):

        if password is None:
            passport = self.get_one_object(username=username)
        else:
            passport = self.get_one_object(username=username, password=get_hash(password))
        return passport

# Passport.objects.get_one_passport(username=username)
class Passport(BaseModel):

    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=40, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')

    # def __init__(self,username,password,email):
    #     self.username = username
    #     self.password = password
    #     self.email = email



    objects = PassportManager()

    class Meta:
        db_table = 's_user_account'

class AddressManager(BaseModelManager):
    def get_default_address(self,passport_id):
        def_addr = self.get_one_object(passport_id = passport_id,is_def = True)
        return def_addr

    def add_one_address(self, passport_id, receive_name, receive_addr, receive_phone,
                        zip_code):
        def_addr = self.get_default_address(passport_id = passport_id)
        if def_addr is None:

            addr = self.create_one_object(passport_id = passport_id,receive_name = receive_name,receive_addr= receive_addr,receive_phone = receive_phone,zip_code = zip_code,is_def = True)
        else:
            addr = self.create_one_object(passport_id = passport_id ,receive_name = receive_name,receive_addr= receive_addr,receive_phone = receive_phone,zip_code = zip_code,)

        return addr


class Address(BaseModel):

    passport = models.ForeignKey('Passport', verbose_name='所属账户')
    receive_name = models.CharField(max_length=20, verbose_name='收件人')
    receive_addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, verbose_name='邮箱')
    receive_phone = models.CharField(max_length=11, verbose_name='联系电话')
    is_def = models.BooleanField(default=False, verbose_name='是否默认')

    objects = AddressManager()
    class Meta:
        db_table = 's_user_address'

class BrowseHistoryLogicManager(BaseModelManager):

    def get_browse_list_by_passport(self, passport_id):
        browsed_li = BrowseHistory.objects.get_browse_list_by_passport(passport_id=passport_id)
        for browsed in browsed_li:
            image = Image.objects.get_image_by_goods_id(goods_id=browsed.goods.id)
            browsed.goods.img_url = image.img_url
        return browsed_li



class BrowseHistoryManager(BaseModelManager):
    def get_one_history(self, passport_id, goods_id):
        history = self.get_one_object(passport_id=passport_id, goods_id=goods_id)
        return history



    def add_one_history(self, passport_id, goods_id):

        history = self.get_one_history(passport_id=passport_id, goods_id=goods_id)
        # print(history)
        if history:
            history.save()
        else:
            history = self.create_one_object(passport_id=passport_id, goods_id=goods_id)
        return history


    def get_browse_list_by_passport(self, passport_id):
        browse_list =  self.get_object_list(filters={'passport_id':passport_id}, order_by=('-update_time',))
        return browse_list


class BrowseHistory(BaseModel):

    goods = models.ForeignKey('df_goods.Goods', verbose_name='所属商品')
    passport = models.ForeignKey('Passport', verbose_name='所属用户')

    objects = BrowseHistoryManager()
    objects_logic = BrowseHistoryLogicManager()
    class Meta:
        db_table = 's_browse_history'



# Create your models here.
