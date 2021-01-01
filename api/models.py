from django.db import models
import django.utils.timezone as timezone


# Create your models here.
class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='創建時間')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新時間')
    is_delete = models.BooleanField(default=False, verbose_name='是否刪除')

    class Meta:
        abstract = True



class Shop(BaseModel):
    name = models.CharField(max_length=256, null=False, verbose_name='館別名稱')

    class Meta:
        db_table = 'shop'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class Product(BaseModel):
    id = models.AutoField(primary_key=True)
    stock_pcs = models.PositiveIntegerField(verbose_name='商品庫存')
    sales = models.IntegerField(default=0, verbose_name='商品銷量')
    price = models.PositiveIntegerField(verbose_name='商品價格')
    shop = models.ForeignKey(
            Shop,
            related_name = 'products',
            on_delete = models.CASCADE  
    )
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class Order(BaseModel):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(
            Product,
            related_name = 'orders',
            on_delete = models.CASCADE  
        )
    
    shop = models.ForeignKey(
            Shop,
            related_name = 'orders',
            on_delete = models.CASCADE  
    )
    qty = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    customer_id = models.CharField(max_length=256, null=False)

    class Meta:
        ordering = ('qty', )
    

    def __str__(self):
        return self.id

