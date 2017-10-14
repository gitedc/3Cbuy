# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('df_user', '0001_initial'),
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(verbose_name='创建时间', auto_now_add=True)),
                ('update_time', models.DateTimeField(verbose_name='更新时间', auto_now=True)),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('goods_count', models.IntegerField(verbose_name='商品数目', default=1)),
                ('goods', models.ForeignKey(to='df_goods.Goods', verbose_name='商品')),
                ('passport', models.ForeignKey(to='df_user.Passport', verbose_name='账户')),
            ],
            options={
                'db_table': 's_cart',
            },
        ),
    ]
