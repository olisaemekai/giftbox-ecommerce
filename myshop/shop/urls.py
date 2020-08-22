from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('box/<int:id>/', views.box_detail, name='box_detail'),
    path('tag/<slug:tag_slug>', views.tag_product_list, name='product_list_by_tag' )
    
]
