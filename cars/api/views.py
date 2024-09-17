from .serializres import CarSerializer, MainPageSerializer
from cars.models import Car
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from main.filter import CarFilter,MainPageFilter
from jp_center.models import FrontCar


class CustomPagination(PageNumberPagination):
    page_size = 20  # Количество объектов на странице
    page_size_query_param = "page_size"  # Параметр для запроса
    max_page_size = 20


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = CarFilter

    def list(self, request, *args, **kwargs):
        # Получаем параметры фильтрации из тела запроса
        filters = request.data.get("filters", {})

        # Применяем фильтрацию
        filtered_queryset = self.filterset_class(filters, queryset=self.queryset)

        # Получаем отфильтрованные данные
        if filtered_queryset.is_valid():
            paginated_queryset = self.paginate_queryset(filtered_queryset.qs)
            serializer = self.get_serializer(paginated_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(
                filtered_queryset.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def get_permissions(self):
        if self.request.method == "GET":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]



    