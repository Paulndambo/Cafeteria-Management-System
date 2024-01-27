from rest_framework import serializers


class SessionCreateSerializer(serializers.Serializer):
    registration_number = serializers.CharField(max_length=255)