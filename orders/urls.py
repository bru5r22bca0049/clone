from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
   
    path('buy-now/<int:id>/', views.buy_now, name='buy_now'),
    
    path('shipping/', views.shipping, name='shipping'),
    
    path('', views.orders, name='orders'),
    
    path('place-order/', views.place_order, name='place_order'),
]