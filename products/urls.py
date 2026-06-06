from django.urls import path
from . import views

urlpatterns = [

    # Home Page
    path('', views.home, name='home'),
    
    path(
        'add-product/',
        views.add_product,
        name='add_product'
    ),
    
    path('search/', views.search_products, name='search'),
     
    path(
        'sell/',
        views.sell_product,
        name='sell_product'
    ),
    
    path(
    'search-suggestions/',
    views.search_suggestions,
    name='search_suggestions'
   ),


    # Product List Page
    path('products/', views.product_list, name='products'),

    # Product Detail
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    # Wishlist Page
    path(
        'wishlist/',
        views.wishlist,
        name='wishlist'
    ),

    # Add to Wishlist
    path(
        'wishlist/add/<int:product_id>/',
        views.add_to_wishlist,
        name='add_to_wishlist'
    ),

    # Remove from Wishlist
    path(
        'wishlist/remove/<int:product_id>/',
        views.remove_from_wishlist,
        name='remove_from_wishlist'
    ),


    path(
    'search-suggestions/',
    views.search_suggestions,
    name='search_suggestions'
    ),
]