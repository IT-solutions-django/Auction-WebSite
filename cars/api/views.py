from .serializres import CarSerializer
from cars.models import Car
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from main.filter import CarFilter



class CustomPagination(PageNumberPagination):
    """Задаем класс пагаинации для апи
    для пагинации на мейн странице будем использовать пагинацию апи"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 20


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    filterset_class = CarFilter

    def list(self, request, *args, **kwargs):
        """Зачем это? Я подумал, что неплохо было бы явно задать логику
        пагинации и фильтрации"""
        
        filters = request.data.get("filters", {})#а это просто, чтобы лаконично реализовать main view
        filtered_queryset = self.filterset_class(filters, queryset=self.queryset)

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
