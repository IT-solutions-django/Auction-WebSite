from django.contrib import admin
from .models import VkSettings,Video,PlayList


admin.site.register((VkSettings,PlayList,Video))


