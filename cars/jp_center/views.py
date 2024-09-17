from django.shortcuts import render
from django.http import JsonResponse
from .models import CarModel


def get_models(request):
    make_id = request.GET.get('make_id')
    if make_id:
        models = CarModel.objects.filter(make_id=make_id).values('id', 'name')
        return JsonResponse(list(models), safe=False)
    return JsonResponse([], safe=False)


