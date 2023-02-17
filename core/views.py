from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from core.serializers import UserSerializer, ProductSerializer, SavedSerializer, CartSerializer, OrderSerializer
from core.models import Product, Saved, Cart, Order, OrderProductInfo


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = UserSerializer(request.user)
        return Response(user.data)

    def patch(self, request):
        user = UserSerializer(request.user, request.data)
        if user.is_valid():
            user.save()
            return Response({'data': 'Updated'})
        return Response({'data': 'Invalid'}, status=400)


class ProductView(APIView):
    def get(self, request):
        productsInstance = Product.objects.all()
        data = ProductSerializer(productsInstance, many=True).data
        return Response({'data': data})


class ProductSaveView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, product_id):
        user_id = request.user.id
        exists = Saved.objects.filter(
            user=user_id, product=product_id).exists()
        if exists:
            return Response({'data': 'Already Saved'})

        products = Product.objects.filter(id=product_id)
        if len(products) == 0:
            return Response({'data': 'Invalid product_id'})

        product = products[0]
        saved = SavedSerializer(data={'product': product.id, 'user': user_id})
        if not saved.is_valid():
            print(saved.errors)
            return Response({'data': 'Invalid'})

        saved.save()
        return Response({'data': 'Saved'})

    def delete(self, request, product_id):
        user_id = request.user.id
        saved_products = Saved.objects.filter(user=user_id, product=product_id)
        if len(saved_products) == 0:
            return Response({'data': 'Is not Saved'})

        saved_products.delete()
        return Response({'data': 'Removed'})


class SavedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        saved_products = Saved.objects.filter(user=user_id)
        data = SavedSerializer(saved_products, many=True).data

        return Response({'data': data})


class CartView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        cart_products = Cart.objects.filter(user=user_id)
        data = CartSerializer(cart_products, many=True).data

        return Response({'data': data})

    def put(self, request):
        user_id = request.user.id
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'data': "'product_id' in body is required"})

        cart_products = Cart.objects.filter(product=product_id, user=user_id)

        if cart_products.exists():
            cart_product = cart_products[0]
            cart_product.quantity += 1
            cart_product.save()
            return Response({'data': "Updated product quantity in cart"})

        products = Product.objects.filter(id=product_id)
        if len(products) == 0:
            return Response({'data': 'Invalid product_id'})

        product = products[0]
        cart = CartSerializer(data={'product': product.id, 'user': user_id})
        if not cart.is_valid():
            print(cart.errors)
            return Response({'data': 'Invalid'})

        cart.save()
        return Response({'data': 'product added to cart'})

    def delete(self, request):
        user_id = request.user.id
        Cart.objects.filter(user=user_id).delete()
        return Response({'data': 'emptied cart'})


class CartProductView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, product_id):
        user_id = request.user.id
        cart_products = Cart.objects.filter(product=product_id, user=user_id)

        if not cart_products.exists():
            return Response({'data': 'Invalid product_id or product not exists'})

        cart_product = cart_products[0]
        if cart_product.quantity == 1:
            cart_product.delete()
            return Response({'data': "Product removed from cart"})

        cart_product.quantity -= 1
        cart_product.save()
        return Response({'data': 'decreased product quantity from cart'})


class CartCheckOutView(APIView):
    def post(self, request):
        user_id = request.user.id
        user_cart_products = Cart.objects.filter(user=user_id)

        if not user_cart_products.exists():
            return Response({'data': 'empty cart'})

        order = Order(user=request.user)
        total = 0
        order.save()
        for cart_product in user_cart_products:
            order.products.add(OrderProductInfo.objects.create(
                product=cart_product.product, quantity=cart_product.quantity))
            total += (cart_product.quantity * cart_product.product.price)
        order.total = total
        order.save()

        user_cart_products.delete()
        return Response({'data': 'order placed'})


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.user.id
        saved_products = Order.objects.filter(user=user_id)
        data = OrderSerializer(saved_products, many=True).data

        return Response({'data': data})
