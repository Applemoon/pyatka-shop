from django.contrib import admin

from .models import Category, Item


class ItemInline(admin.TabularInline):
    model = Item


class ItemAdmin(admin.ModelAdmin):
    list_filter = ['needed', 'bought', 'category', 'important']
    list_display = ('name', 'needed', 'bought', 'category', 'important')
    search_fields = ['name']


class CategoryInline(admin.TabularInline):
    model = Category


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'full_name']
    list_display = ('full_name', 'name', 'position', 'items_count')
    inlines = [ItemInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
