from haystack import  indexes
from df_goods.models import Goods

class Goodsindex(indexes.Indexable, indexes.SearchIndex):

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Goods

    def index_queryset(self, using=None):
        goods_li = self.get_model().objects.all()
        return goods_li







