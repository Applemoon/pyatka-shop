from django.urls import path
from . import views

urlpatterns = [
    path('items', views.ItemList.as_view(), name='items'),
    path('items/<int:pk>', views.ItemDetail.as_view(), name='item_detail'),
    path('categories', views.CategoryList.as_view(), name='categories'),
    path('all_not_bought', views.all_not_bought, name='all_not_bought'),
]
