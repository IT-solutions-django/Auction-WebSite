"""
URL configuration for settings project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from jp_center.views import get_models
from django.conf import settings
from django.conf.urls.static import static
from main.views import frontcar_list_view,playlist_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-models/', get_models, name='get_models'),
    path('api/',include('api.urls'),name = 'api'),
    path('catalog/', frontcar_list_view, {'page': 1}, name='catalog_default'),
    path('catalog/page/<int:page>/',frontcar_list_view,name='catalog'),
    path('playlist/',playlist_view,name='main')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)