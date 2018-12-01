from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.utils.datastructures import MultiValueDictKeyError
from json.decoder import JSONDecodeError
from django.core.exceptions import ValidationError
import json

from .models import Item


@require_GET
def items(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    raw_items = Item.objects.filter()
    items = [raw_item.getDict() for raw_item in raw_items]
    return JsonResponse(items, safe=False)


@require_POST
def add_item(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
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
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    try:
        item_id = json.loads(request.body)['item_id']
    except (MultiValueDictKeyError, JSONDecodeError):
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    item.needed = not item.needed
    item.save()
    return JsonResponse({"status": "ok"})


@require_POST
def toggle_starred(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    try:
        item_id = json.loads(request.body)['item_id']
    except (MultiValueDictKeyError, JSONDecodeError):
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    item.starred = not item.starred
    item.save()
    return JsonResponse({"status": "ok"})


@require_POST
def toggle_bought(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
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
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    try:
        item_id = json.loads(request.body)['item_id']
    except (MultiValueDictKeyError, JSONDecodeError):
        return HttpResponse(status=400)
    item = get_object_or_404(Item, pk=item_id)
    item.delete()
    return JsonResponse({"status": "ok"})


@require_POST
def rename(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
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
