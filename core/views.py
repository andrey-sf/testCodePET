from django.core.cache import cache
from django.conf import settings
from django.db.models import Sum
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from rest_framework.pagination import LimitOffsetPagination


class CollectViewSet(ModelViewSet):
    """
    ViewSet для работы с моделью Collect.

    Предоставляет операции CRUD (Create, Retrieve, Update, Delete).
    Поддерживает постраничную навигацию и кэширование.
    """
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    pagination_class = LimitOffsetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user)
        self.update_cache()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        self.update_cache()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        self.update_cache()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update_cache(self):
        # Очистить кэш после изменения данных
        cache.clear()


class PaymentViewSet(ModelViewSet):
    """
    ViewSet для работы с моделью Payment.
    Предоставляет операции CRUD (Create, Retrieve, Update, Delete).
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_payment = serializer.save()
        collect = updated_payment.collect
        collect.collected_amount = Payment.objects.filter(collect=collect).aggregate(total_amount=Sum('amount'))[
            'total_amount']
        collect.save()
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def collect(self, request, pk=None):
        """
        Получает список всех платежей для определенного сбора.
        """
        try:
            collect = Collect.objects.get(pk=pk)
        except Collect.DoesNotExist:
            return Response({"error": "Collect с таким номером не существует."}, status=status.HTTP_404_NOT_FOUND)

        payments = Payment.objects.filter(collect=collect)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data)

