from django.contrib import admin
from django.contrib.admin import DateFieldListFilter, FieldListFilter
from .models import (
    User,
    Bouquet,
    Occasion,
    Composition,
    Order,
    Color,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id_tg', 'name', 'registered_at',)
    search_fields = ('name',)
    list_filter = (('registered_at', DateFieldListFilter),)


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'occasion','color',)
    search_fields = ('name',)
    list_filter = ('price', 'occasion',)
    filter_horizontal = ('composition',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bouquet', 'phone', 'address', 'is_deliverd', 'order_date', 'delivery_date')
    list_filter = ('is_deliverd', ('delivery_date', DateFieldListFilter), ('order_date', DateFieldListFilter), 'bouquet')
    search_fields = ('user__name', 'bouquet__name')


@admin.register(Occasion)
class OccasionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)