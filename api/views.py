from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from json.decoder import JSONDecodeError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
import json

from .models import Category, Item
from .serializers import CategorySerializer, ItemSerializer

ok_response = JsonResponse({"status": "ok"})


@login_required
@api_view(['GET'])
def items(request):
    items = Item.objects.all()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)


@login_required
@api_view(['GET'])
def categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def add_item(request):
    try:
        data = request.POST
        name = data['name']
        if len(name) > 100:  # TODO bad checking here
            return HttpResponse(status=HTTP_400_BAD_REQUEST)
        needed = json.loads(data.get('needed', 'false'))
        category_name = data.get('category', Category.default_name)
        category = get_object_or_404(Category, name=category_name)
        item = Item.objects.create(name=name, needed=needed, category=category)
    except (MultiValueDictKeyError, JSONDecodeError, ValidationError):
        return HttpResponse(status=HTTP_400_BAD_REQUEST)

    serializer = ItemSerializer(item)
    return Response(serializer.data)


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
