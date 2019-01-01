from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer

ok_response = JsonResponse({"status": "ok"})


class ItemsList(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                generics.GenericAPIView):
    """
    Get all items or create one.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CategoriesList(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    """
    Get all categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@require_POST
def set_needed(request):
    try:
        item_id = request.POST['item_id']
    except MultiValueDictKeyError:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    item = get_object_or_404(Item, pk=item_id)
    item.needed = True
    item.save()
    return ok_response


@require_POST
def set_not_needed(request):
    try:
        item_id = request.POST['item_id']
    except MultiValueDictKeyError:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    item = get_object_or_404(Item, pk=item_id)
    item.needed = False
    item.save()
    return ok_response


@require_POST
def set_bought(request):
    try:
        item_id = request.POST['item_id']
    except MultiValueDictKeyError:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    item = get_object_or_404(Item, pk=item_id)
    item.bought = True
    item.save()
    return ok_response


@require_POST
def set_not_bought(request):
    if 'item_id' in request.POST:
        try:
            item_id = request.POST['item_id']
        except MultiValueDictKeyError:
            return HttpResponse(status=HTTP_400_BAD_REQUEST)
        item = get_object_or_404(Item, pk=item_id)
        item.bought = False
        item.save()
    else:
        Item.objects.filter(bought=True).update(bought=False)
    return ok_response


@require_POST
def remove(request):
    try:
        item_id = request.POST['item_id']
    except MultiValueDictKeyError:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return ok_response


@require_POST
def rename(request):
    try:
        data = request.POST
        item_id = data['item_id']
        name = data['name']
    except MultiValueDictKeyError:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    item = get_object_or_404(Item, pk=item_id)
    item.name = name
    item.save()
    return ok_response


@require_POST
def change_category(request):
    try:
        data = request.POST
        item_id = data['item_id']
        category = data['category']
    except MultiValueDictKeyError:
        return HttpResponse(status=HTTP_400_BAD_REQUEST)
    item = get_object_or_404(Item, pk=item_id)
    category = get_object_or_404(Category, name=category)
    item.category = category
    item.save()
    return ok_response
