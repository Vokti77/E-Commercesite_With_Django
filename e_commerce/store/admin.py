from django.contrib import admin
from store.models import Category, Product, ProductImage, VariationValue


class ProductImagesAdmin(admin.StackedInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]   # this line write when we create ProductImagesAdmin class for upload ProductImages at the same time when product image upoad
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(VariationValue)

