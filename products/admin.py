from django.contrib import admin
from .models import Product, Category, Wishlist


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Wishlist)

# Register your models here.

