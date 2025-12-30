from rest_framework import serializers


class GenerateVerificationCodeSerializer(serializers.Serializer):
    registration_number = serializers.CharField(max_length=100)


class CodeVerificationSerializer(serializers.Serializer):
    registration_number = serializers.CharField(max_length=100)
    verification_code = serializers.CharField(max_length=10)
