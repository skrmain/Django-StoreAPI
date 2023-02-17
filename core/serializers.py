from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Product, Saved, Cart


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        read_only_fields = ['id', 'username']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'brand', 'category', 'description')


class SavedSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.FloatField(
        source='product.price', read_only=True)

    class Meta:
        model = Saved
        fields = ('user', 'product', 'product_name', 'product_price')


class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.FloatField(
        source='product.price', read_only=True)

    class Meta:
        model = Cart
        fields = ('user', 'product', 'quantity',
                  'product_name', 'product_price')
