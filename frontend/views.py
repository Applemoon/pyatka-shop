from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required


@require_GET
@login_required
def index(request):
    return render(request, 'frontend/index.html')
