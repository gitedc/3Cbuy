from django.conf.urls import url
from df_goods import views
urlpatterns = [
    url(r'^$',views.home_list_page),
    url(r'^goods/(\d+)/$',views.goods_detail),
    url(r'^list/(\d+)/(\d+)/$',views.goods_list),
    url(r'^get_image_list/$',views.get_iamge_list),
]