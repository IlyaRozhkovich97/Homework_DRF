from rest_framework import serializers

from users.models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для платежей
    """

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    Класс сериализатора для пользователя
    """
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
