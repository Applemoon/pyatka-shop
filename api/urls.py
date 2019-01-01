from django.urls import path
from . import views

urlpatterns = [
    path('items', views.ItemsList.as_view(), name='items'),
    path('categories', views.CategoriesList.as_view(), name='categories'),
    path('set_bought', views.set_bought, name='set_bought'),
    path('set_not_bought', views.set_not_bought, name='set_not_bought'),
    path('set_needed', views.set_needed, name='set_needed'),
    path('set_not_needed', views.set_not_needed, name='set_not_needed'),
    path('remove', views.remove, name='remove'),
    path('rename', views.rename, name='rename'),
    path('change_category', views.change_category, name='change_category'),
]
