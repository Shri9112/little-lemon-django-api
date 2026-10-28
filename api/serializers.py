from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Booking, MenuItem

User = get_user_model()

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "inventory"]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "name", "no_of_guests", "booking_date", "user"]
        read_only_fields = ["id", "user"]

    def validate_no_of_guests(self, value):
        if value < 1:
            raise serializers.ValidationError("At least one guest is required.")
        return value

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
