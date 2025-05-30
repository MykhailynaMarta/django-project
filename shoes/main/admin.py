from django.contrib import admin
from.models import *

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('c_name', 'c_description')
    prepopulated_fields = {'c_slug': ('c_name',)}

class ShoesAdmin(admin.ModelAdmin):
    list_display = ('sh_name', 'sh_model', 'sh_size', 'sh_color', 'sh_manufacturer', 'sh_count', 'sh_price', 'sh_gender', 'collection')
    prepopulated_fields = {'sh_slug': ('sh_name',)}

admin.site.register(Shoes, ShoesAdmin)
# admin.site.register(ShoeImage)
admin.site.register(Orders)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(CollectionImage)
# admin.site.register(Orders)

