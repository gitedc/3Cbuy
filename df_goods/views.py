from django.shortcuts import render
from django.core.paginator import Paginator
from df_goods.models import Goods, Goods_Info,Image
from df_user.models import BrowseHistory
from df_goods.enums import *
from django.http import JsonResponse

# Create your views here.
def home_list_page(request):
    fruits_new = Goods.objects.get_goods_list_by_type(goods_type_id=FRUIT, limit=3,sort='new')
    fruits = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FRUIT, limit=4)

    seafoods_new = Goods.objects.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=3, sort='new')
    seafoods = Goods.objects_logic.get_goods_list_by_type(goods_type_id=SEAFOOD, limit=4)

    meats_new = Goods.objects.get_goods_list_by_type(goods_type_id=MEAT, limit=3, sort='new')
    meats = Goods.objects_logic.get_goods_list_by_type(goods_type_id=MEAT,limit=4)

    eggs_new = Goods.objects.get_goods_list_by_type(goods_type_id=EGGS,limit=3,sort='new')
    eggs = Goods.objects_logic.get_goods_list_by_type(goods_type_id=EGGS,limit=4)

    vegetables_new = Goods.objects.get_goods_list_by_type(goods_type_id=VEGETABLES,limit=3,sort='new')
    vegetables = Goods.objects_logic.get_goods_list_by_type(goods_type_id=VEGETABLES,limit=4)

    frozens_new = Goods.objects.get_goods_list_by_type(goods_type_id=FROZEN,limit=3,sort='new')
    frozens = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FROZEN,limit=4)

    context = {'fruits_new':fruits_new,'fruits':fruits,'seafoods_new':seafoods_new,'seafoods':seafoods,
               'meats_new':meats_new,'meats':meats,'vegetables_new':vegetables_new,'vegetables':vegetables,
               'frozens_new':frozens_new,'frozens':frozens,'eggs_new':eggs_new,'eggs':eggs}

    return render(request, 'index.html', context)

def goods_detail(request,goods_id):

    goods = Goods.objects_logic.get_goods_by_id(goods_id=goods_id)
    goods_new = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FRUIT,limit=2,sort='new')

    if request.session.has_key('is_login'):
        passport_id = request.session.get('passport_id')
        # print(type(passport_id))
        BrowseHistory.objects.add_one_history(passport_id=passport_id, goods_id=int(goods_id))
    goods_type = GOODS_TYPE[goods.goods_type_id]

    return render(request,'detail.html',{'goods':goods,'goods_new':goods_new,'goods_type':goods_type})

def goods_list(request,goods_type_id,page_index):

    sort = request.GET.get('sort', 'default')

    goodslist = Goods.objects_logic.get_goods_list_by_type(goods_type_id=goods_type_id, sort = sort)
    paginator =  Paginator(goodslist, 1)
    goodslist = paginator.page(int(page_index))
    pages = paginator.page_range
    current_num = int(page_index)
    num_pages = paginator.num_pages
    if num_pages <= 5:
        pages = range(1, num_pages+1)
    elif current_num <= 3:
        pages = range(1, 6)
    elif num_pages - current_num <= 2:
        pages = range(num_pages-4,num_pages+1)
    else:
        pages = range(current_num-2, current_num+3)



    goods_new = Goods.objects_logic.get_goods_list_by_type(goods_type_id=FRUIT, limit=2, sort='new')
    type_title = GOODS_TYPE[int(goods_type_id)]
    return render(request,'list.html',{'goodslist':goodslist,'goods_new':goods_new
                                       ,'type_title':type_title,'type_id':goods_type_id
                                       ,'sort':sort,'pages':pages})

def get_iamge_list(request):
    goods_id_list = request.GET.get('goods_id_list')
    goods_id_list = goods_id_list.split(',')
    images = Image.objects.get_images_by_goods_id_list(goods_id_list = goods_id_list)
    img_dict = {}
    for image in images:
        img_dict[image.goods.id] = image.img_url.name
    return JsonResponse({'img_dict':img_dict})


