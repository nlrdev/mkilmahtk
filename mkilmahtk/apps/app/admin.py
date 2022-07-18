from django.contrib import admin
from .models import *


class AH_DumpAdmin(admin.ModelAdmin):
    pass

class AH_ItemAdmin(admin.ModelAdmin):
    search_fields = ['a_id', 'item_id',]

class ItemAdmin(admin.ModelAdmin):
    search_fields = ['item_id', 'name',]


admin.site.register(AH_Dump, AH_DumpAdmin)
admin.site.register(AH_Item, AH_ItemAdmin)
admin.site.register(Item, ItemAdmin)