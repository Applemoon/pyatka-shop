from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from json.decoder import JSONDecodeError
import json

from .models import Category, Item

ok_response = JsonResponse({"status": "ok"})


@login_required
@require_GET
def items(request):
    raw_items = Item.objects.all()
    items = [raw_item.getDict() for raw_item in raw_items]
    return JsonResponse(items, safe=False)


@login_required
@require_GET
def categories(request):
    raw_categories = Category.objects.all()
    categories = [raw_category.getDict() for raw_category in raw_categories]
    return JsonResponse(categories, safe=False)


@require_POST
def add_item(request):
    try:
        data = request.POST
        name = data['name']
        if len(name) > 100:  # TODO bad checking here
            return HttpResponse(status=400)
        needed = json.loads(data.get('needed', 'false'))
        category_name = data.get('category', Category.default_name)
        category = get_object_or_404(Category, name=category_name)
        item = Item.objects.create(name=name, needed=needed, category=category)
    except (MultiValueDictKeyError, JSONDecodeError, ValidationError):
        return HttpResponse(status=400)

    return JsonResponse(item.getDict())


@require_POST
def set_needed(request):
    try:
        item_id = request.POST['item_id']
    except MultiValueDictKeyError:
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    item.needed = True
    item.save()
    return ok_response


@require_POST
def set_not_needed(request):
    try:
        item_id = request.POST['item_id']
    except MultiValueDictKeyError:
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    item.needed = False
    item.save()
    return ok_response


@require_POST
def set_bought(request):
    try:
        item_id = request.POST['item_id']
    except MultiValueDictKeyError:
        return HttpResponse(status=400)
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
            return HttpResponse(status=400)
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
        return HttpResponse(status=400)
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
        return HttpResponse(status=400)
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
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    category = get_object_or_404(Category, name=category)
    item.category = category
    item.save()
    return ok_response
