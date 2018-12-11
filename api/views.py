from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from json.decoder import JSONDecodeError
import json

from .models import Category, Item


@login_required(login_url='/pyatka/login')
@require_GET
def items(request):
    raw_items = Item.objects.all()
    items = [raw_item.getDict() for raw_item in raw_items]
    return JsonResponse(items, safe=False)


@login_required(login_url='/pyatka/login')
@require_GET
def categories(request):
    raw_categories = Category.objects.all()
    categories = [raw_category.getDict() for raw_category in raw_categories]
    return JsonResponse(categories, safe=False)


@require_POST
def add_item(request):
    try:
        data = json.loads(request.body)
        name = data['name']
        if len(name) > 100:  # TODO bad checking here
            return HttpResponse(status=400)
        needed = data.get('needed', False)
        item = Item(name=name, needed=needed)
        item.save()
    except (MultiValueDictKeyError, JSONDecodeError, ValidationError):
        return HttpResponse(status=400)

    return JsonResponse(item.getDict())


@require_POST
def toggle_needed(request):
    try:
        item_id = json.loads(request.body)['item_id']
    except (MultiValueDictKeyError, JSONDecodeError):
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    item.needed = not item.needed
    item.save()
    return JsonResponse({"status": "ok"})


@require_POST
def toggle_bought(request):
    try:
        item_id = json.loads(request.body)['item_id']
    except (MultiValueDictKeyError, JSONDecodeError):
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    item.bought = not item.bought
    item.save()
    return JsonResponse({"status": "ok"})


@require_POST
def remove(request):
    try:
        item_id = json.loads(request.body)['item_id']
    except (MultiValueDictKeyError, JSONDecodeError):
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return JsonResponse({"status": "ok"})


@require_POST
def rename(request):
    try:
        data = json.loads(request.body)
        item_id = data['item_id']
        name = data['name']
    except (MultiValueDictKeyError, JSONDecodeError):
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    item.name = name
    item.save()
    return JsonResponse({"status": "ok"})


@require_POST
def change_category(request):
    try:
        data = json.loads(request.body)
        item_id = data['item_id']
        category = data['category']
    except (MultiValueDictKeyError, JSONDecodeError):
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    category = get_object_or_404(Category, name=category)
    item.category = category
    item.save()
    return JsonResponse({"status": "ok"})
