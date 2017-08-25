from django.shortcuts import render
from .forms import SubscriberForm
from products.models import *

# Create your views here.
def fairypresent(request):
    name = "AblAlx"
    current_day = "01.08.2017"
    form = SubscriberForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        print (request.POST)
        print(form.cleaned_data)
        print(form.cleaned_data["name"])
        new_form = form.save()

    return render(request,'fairypresent/fairypresent.html',locals())

def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    products_images_pumphead = products_images.filter(product__category=1)
    products_images_valfdordoll = products_images.filter(product__category=2)
    products_images_other = products_images.filter(product__category=3)
    products_images_sleepdoll = products_images.filter(product__category=4)

    return render(request,'fairypresent/home.html',locals() )