import requests
import math
from django.shortcuts import render
from jp_center.models import CarContainer
from .forms import CarFilterForm
from .forms import CarFilterForm
from youtube.models import Playlist
from urllib.parse import urlparse, parse_qs


def frontcar_list_view(request, page=1):
    form = CarFilterForm(request.GET or None)
    url = f"http://localhost:8000/api/cars/?page={page}"

    filters = {}
    fields = [
        "make",
        "model",
        "privod",
        "kpp",
        "color",
        "mileage_min",
        "mileage_max",
        "power_min",
        "power_max",
        "price_min",
        "price_max",
        "year_min",
        "year_max",
        "volume_min",
        "volume_max",
    ]

    if form.is_valid():
        for field in fields:
            value = form.cleaned_data.get(field)
            if value:
                if field in ["make", "model"]:
                    filters[field] = value.name
                else:
                    filters[field] = value

    page = request.GET.get("page", 1)

    filters["page"] = page
    data = {"filters": filters}

    response = requests.get(url, json=data)
    print(data)
    if response.status_code == 200:
        result = response.json()
        cars = result.get("results", [])
        next_page = result.get("next", [])
        previous_page = result.get("previous", [])
    else:
        cars = []
        next_page = []
        previous_page = []
    if next_page:
        next_page = urlparse(next_page)
        next_page = parse_qs(next_page.query)
        next_page = next_page.get("page", None)[0]
    if previous_page:
        previous_page = urlparse(previous_page)
        previous_page = parse_qs(previous_page.query)
        if next_page != "3":
            previous_page = previous_page.get("page", None)[0]
        else:
            previous_page = "1"

    return render(
        request,
        "main/frontcar_list.html",
        {
            "form": form,
            "object_list": cars,
            "next": next_page,
            "previous": previous_page,
        },
    )


def playlist_view(request):
    playlist = Playlist.objects.get(name="main")
    containers = CarContainer.objects.all()
    return render(
        request, "main/main_page.html", {"playlist": playlist, "containers": containers}
    )
