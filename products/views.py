from django.shortcuts import render
from products.models import *

def product(request,product_id):
    # products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    # products_images_pumphead = products_images.filter(product__category=1)
    # products_images_valfdordoll = products_images.filter(product__category=2)
    # products_images_other = products_images.filter(product__category=3)
    # products_images_sleepdoll = products_images.filter(product__category=4)
    product = Product.objects.get(id=product_id)

    return render(request,'products/product.html',locals() )