from django.urls import path
from . import views

urlpatterns = [
    path('items', views.items, name='items'),
    path('add_item', views.add_item, name='add_item'),
    path('toggle_needed', views.toggle_needed, name='toggle_needed'),
    path('toggle_bought', views.toggle_bought, name='toggle_bought'),
    path('remove', views.remove, name='remove'),
    path('rename', views.rename, name='rename'),
    path('change_category', views.change_category, name='change_category'),
    path('categories', views.categories, name='categories'),
]
