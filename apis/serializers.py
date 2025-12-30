from rest_framework import serializers
from apps.students.models import Student

class StudentSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = "__all__"

    
    def get_balance(self, obj):
        return obj.studentwallet.balance
    
    def get_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"


class MpesaCallbackSerializer(serializers.Serializer):
    Body = serializers.JSONField()


class MpesaSTKPushSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class ConfirmPaymentSerializer(serializers.Serializer):
    MerchantRequestID = serializers.CharField(max_length=255)
    CheckoutRequestID = serializers.CharField(max_length=255)
    cart_items = serializers.ListField(child=serializers.JSONField())
    registration_number = serializers.CharField(max_length=50)
    wallet_balance_used = serializers.DecimalField(max_digits=10, decimal_places=2)
    mpesa_amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderConfirmationSerializer(serializers.Serializer):
    cart_items = serializers.ListField(child=serializers.JSONField())
    registration_number = serializers.CharField(max_length=50)
    wallet_balance_used = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)
    cash_amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0)