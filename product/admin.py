from django.contrib import admin
from .models import Banner,Category, Brand, Color,  Size, Product

class BrandAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(Brand,BrandAdmin)

admin.site.register(Size)

class BannerAdmin(admin.ModelAdmin):
    list_display=('alt_text', 'image_tag')
admin.site.register(Banner,BannerAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display=('title', 'image_tag')
admin.site.register(Category,CategoryAdmin)

class ColorAdmin(admin.ModelAdmin):
    list_display=('title', 'color_bg')
admin.site.register(Color,ColorAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('id', 'vendor', 'title', 'brand', 'image_tag','color_bg', 'size', 'quantity' ,'price_not', 'price', 'status', 'is_featured')
    list_editable=('status','is_featured')
admin.site.register(Product,ProductAdmin)



