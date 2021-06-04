from django.contrib import admin
from .models import *

class ItemVariationAdmin(admin.ModelAdmin):
    list_display = ["variation", "value", "attachment"]
    list_filter = ["variation", "variation__item"]
    search_fields = ["value"]


class ItemVariationInLineAdmin(admin.TabularInline):
    model = ItemVariation
    extra = 1


class VariationAdmin(admin.ModelAdmin):
    list_display = ["item", "name"]
    list_filter = ["item"]
    search_fields = ["name"]
    inlines = [ItemVariationInLineAdmin]


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Coupon)
admin.site.register(ItemVariation, ItemVariationAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ItemImage)