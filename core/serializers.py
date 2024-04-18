from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import Collect, Payment, Person


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.name', read_only=True)
    collect = serializers.PrimaryKeyRelatedField(queryset=Collect.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'timestamp', 'collect']

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Сумма платежа не может быть отрицательной")
        return value

    def create(self, validated_data):
        collect = validated_data.pop('collect')
        return Payment.objects.create(collect=collect, **validated_data)


class CollectSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Collect
        fields = ['id', 'author', 'title', 'occasion', 'description', 'target_amount', 'collected_amount',
                  'contributors_count', 'cover_image', 'end_datetime', 'payments']
        read_only_fields = ['author']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)


class PersonCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = Person
        fields = ("id", "email", "name", "password")
        read_only_fields = ("id",)


class PersonDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "email", "name", "password")
        read_only_fields = ("id", "email", "name", "password")
