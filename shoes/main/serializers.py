from rest_framework import serializers # Import the serializer class
from .models import Orders, Shoes, Order_status  # Import the Note model

# Create a serializer class
# This class will convert the Note model into JSON
class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'

class ShoesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shoes
        fields = '__all__'

class Order_statusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_status
        fields = '__all__'