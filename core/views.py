from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer
from rest_framework.response import Response
from django.db.models import Sum


class CollectViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с моделью Collect.

    Предоставляет операции CRUD (Create, Retrieve, Update, Delete).
    Поддерживает кэширование списка и детального представлений на 15 минут.

    """
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [IsAuthenticated]

    # @method_decorator(cache_page(60 * 15))  # Кэш на 15 минут
    def list(self, request, *args, **kwargs):
        """
        Получает список всех сборов.

        Кэширует список на 15 минут.

        """
        return super().list(request, *args, **kwargs)

    # @method_decorator(cache_page(60 * 15))  # Кэш на 15 минут
    def retrieve(self, request, *args, **kwargs):
        """
        Получает детальное представление сбора по его идентификатору.

        Кэширует детальное представление на 15 минут.

        """
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PaymentViewSet(ModelViewSet):
    """
    ViewSet для работы с моделью Payment.
    Предоставляет операции CRUD (Create, Retrieve, Update, Delete).
    Поддерживает кэширование списка и детальных представлений на 15 минут.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    # @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        """
        Получает список всех платежей.
        Кэширует список на 15 минут.
        """
        return super().list(request, *args, **kwargs)

    # @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        """
        Получает детальное представление платежа по его идентификатору.
        Кэширует детальное представление на 15 минут.
        """
        return super().retrieve(request, *args, **kwargs)

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
