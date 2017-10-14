from django.conf.urls  import url
from df_user import  views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register),
    url(r'^login/$', views.login),
    url(r'^register_check/$',views.register_check),
    url(r'^login_check/$',views.login_check),
    url(r'^address/$',views.address),
    url(r'^test1/$', views.test1),
    url(r'^test2/$', views.test2),
    url(r'^logout/$', views.logout),
    url(r'^usercenter/$',views.usercenter),
    url(r'^order/$', views.order),
]

















