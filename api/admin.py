from django.contrib import admin

from .models import Item


class ItemInline(admin.TabularInline):
    model = Item


class ItemAdmin(admin.ModelAdmin):
    list_filter = ['needed', 'starred', 'bought', 'category']
    list_display = ('name', 'needed', 'starred', 'bought', 'category')
    search_fields = ['name']


admin.site.register(Item, ItemAdmin)
