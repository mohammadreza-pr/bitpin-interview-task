from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value
    
    def create(self, validated_data):
        
        validated_data['password'] = make_password(validated_data['password'])  # Hash the password
        return super().create(validated_data)
    
    