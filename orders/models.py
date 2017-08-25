from django.db import models
from products.models import Product
from  django.db.models.signals import post_save


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    dt_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return "Статус  %s" % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
     total_price     = models.DecimalField(max_digits=10,decimal_places=2,default=0)  # total price for allproduct in order
     custom_name = models.CharField(max_length=64, blank=True, null=True ,default=None)
     custom_email = models.EmailField(blank=True, null=True ,default=None)
     custom_phone = models.CharField(max_length=48, blank=True, null=True ,default=None)
     custom_address = models.CharField(max_length=128, blank=True, null=True ,default=None)
     status = models.ForeignKey(Status)
     dt_created = models.DateTimeField(auto_now=False,auto_now_add=True)
     dt_updated = models.DateTimeField(auto_now=True,auto_now_add=False)
     comments = models.TextField(blank=True, null=True ,default=None)

     def __str__(self):
         return "Заказ  %s %s" %(self.id,self.status.name)

     def save(self, *args, **kwargs):
         super(Order, self).save(*args, **kwargs)



     class Meta:
         verbose_name = 'Заказ'
         verbose_name_plural = 'Заказы'


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None)
    product = models.ForeignKey(Product, blank=True, null=True, default=None)
    nmb = models.IntegerField(default=1)
    price_per_item =  models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)#price * nmb
    is_active = models.BooleanField(default=True)
    dt_created = models.DateTimeField(auto_now=False, auto_now_add=True)
    dt_updated = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = self.nmb * price_per_item
        super(ProductInOrder, self).save(*args, **kwargs)

def product_in_order_post_save(sender, instance, created, **kwargs):
        order = instance.order
        all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

        order_total_price = 0
        for item in all_products_in_order:
            order_total_price += item.total_price

        instance.order.total_price = order_total_price
        instance.order.save(force_update=True)

post_save.connect(product_in_order_post_save, sender=ProductInOrder)