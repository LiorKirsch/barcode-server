from django.contrib import admin

from models import Product, ProductImage, Scanner, ScannedProducts

admin.site.register(Scanner)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ScannedProducts)