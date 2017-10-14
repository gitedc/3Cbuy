# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('goods_type_id', models.SmallIntegerField(default=1, choices=[(1, '新鲜水果'), (2, '海鲜水产'), (3, '猪牛羊肉'), (4, '禽肉蛋品'), (5, '新鲜蔬菜'), (6, '速冻食品')], verbose_name='商品类型id')),
                ('goods_name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('goods_sub_title', models.CharField(max_length=256, verbose_name='商品副标题')),
                ('goods_price', models.DecimalField(max_digits=10, verbose_name='商品价格', decimal_places=2)),
                ('transit_price', models.DecimalField(max_digits=10, verbose_name='商品运费', decimal_places=2)),
                ('goods_unite', models.CharField(max_length=20, verbose_name='商品单位')),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品描述')),
                ('goods_stock', models.IntegerField(default=0, verbose_name='商品库存')),
                ('goods_sales', models.IntegerField(default=0, verbose_name='商品销量')),
                ('goods_status', models.SmallIntegerField(default=1, verbose_name='商品状态')),
            ],
            options={
                'db_table': 's_goods',
            },
        ),
        migrations.CreateModel(
            name='Goods_Info',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('goods_info', tinymce.models.HTMLField(verbose_name='商品描述')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('img_url', models.ImageField(verbose_name='图片路径', upload_to='goods/')),
                ('is_def', models.BooleanField(default=False, verbose_name='是否默认')),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='所属商品')),
            ],
            options={
                'db_table': 's_goods_image',
            },
        ),
    ]
