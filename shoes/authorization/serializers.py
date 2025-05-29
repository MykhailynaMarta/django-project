from rest_framework import serializers # Import the serializer class
from .models import CustomUser  # Import the Note model

# Create a serializer class
# This class will convert the Note model into JSON
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'