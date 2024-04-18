from django.core.cache import cache
from django.conf import settings
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Collect, Payment
from .serializers import CollectSerializer, PaymentSerializer


class CollectViewSet(ModelViewSet):
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        cache_key = 'collect_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, settings.CACHE_TTL)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        cache_key = f'collect_{kwargs["pk"]}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cache.set(cache_key, serializer.data, settings.CACHE_TTL)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        cache.delete('collect_list')


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        cache_key = 'payment_list'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, settings.CACHE_TTL)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        cache_key = f'payment_{kwargs["pk"]}'
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        cache.set(cache_key, serializer.data, settings.CACHE_TTL)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.delete('payment_list')

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
        cache.delete('collect_list')
        return Response(serializer.data)
