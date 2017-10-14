from django.conf.urls import url
from df_cart import views


urlpatterns = [
    url(r'^add/$', views.cart_add),
    url(r'^count/$', views.cart_count),
    url(r'^cart/$',views.cart_show),
    url(r'^update/$', views.cart_update),
    url(r'^del/$', views.cart_del),
]