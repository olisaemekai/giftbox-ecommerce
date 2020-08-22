from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Tag, BoxItem, Box
from cart.forms import CartAddProductForm

from .forms import SearchProductForm
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.db.models import Q


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    custom_boxes = Box.objects.filter(custom=True)
    search_form = SearchProductForm()

    accessories = Category.objects.get(name__iexact='Accessories')
    edibles = Category.objects.get(name__iexact='Edibles')
    fashion = Category.objects.get(name__iexact='Fashion')
    fragrances = Category.objects.get(name__iexact='Fragrances')
    gadgets = Category.objects.get(name__iexact='Gadgets')
    # first_item = []
    # for category in categories:
    #     if category.products.all().exists():
    #         first_item.append(category.products.all()[0]) 
    

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'custom_boxes': custom_boxes,
        'search_form': search_form,
        'accessories': accessories.tags.all(),
        'edibles': edibles.tags.all(),
        'fashion': fashion.tags.all(),
        'fragrances': fragrances.tags.all(),
        'gadgets': gadgets.tags.all(),
    }
    return render(request, 'shop/product/list.html', context)

def tag_product_list(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    tag_items = tag.product_set.all()

    cart_product_form = CartAddProductForm(initial={'quantity': 1})

    context = {
        'tag_items': tag_items,
        'cart_product_form': cart_product_form,
    }
    return render(request, 'shop/product/tag_product.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm(initial={'quantity': 1})
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        }
    return render(request, 'shop/product/detail.html', context)


def box_detail(request, id):
    box = get_object_or_404(Box, id=id, custom=True)
    cart_product_form = CartAddProductForm(initial={'quantity': 1})
    context = {
        'box': box,
        'cart_product_form': cart_product_form,
        }
    return render(request, 'shop/product/box_detail.html', context)
# @require_POST
# def search(request):
#     search = SearchProductForm()
#     if search.is_valid():
#         cd = search.cleaned_data['search']
#         products = Product.objects.filter(name__icontains=cd)
#         return(request, 'shop/product/search.html', {'products': products})

class SearchResultsView(ListView):
    model = Product
    template_name = 'shop/product/search.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(Q(name__icontains=query))
        return object_list