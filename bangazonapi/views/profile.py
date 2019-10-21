"""View module for handling requests about customer profiles"""
import datetime
from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from .order import OrderSerializer
from .product import ProductSerializer
from bangazonapi.models import Order, Customer, Product, OrderProduct


class CartProductSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for products

    Arguments:
        serializers
    """
    class Meta:
        model = Product
        url = serializers.HyperlinkedIdentityField(
            view_name='product',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'price', 'description',
                  'location', 'category',)
        depth = 1

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customer profile

    Arguments:
        serializers
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        depth = 1


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customer profile

    Arguments:
        serializers
    """
    user = UserSerializer(many=False)

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id',
        )
        fields = ('id', 'url', 'user', 'phone_number', 'address', 'payment_types')
        depth = 1


class Profile(ViewSet):
    """Request handlers for user profile info in the Bangazon Platform"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def list(self, request):
        """Handle GET requests for a user profile

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            current_user = Customer.objects.get(user=request.auth.user)
            serializer = ProfileSerializer(current_user, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    @action(methods=['get', 'put', 'delete'], detail=False)
    def cart(self, request):
        """Shopping cart route for customers

        Returns:
            Response -- An HTTP response
        """
        current_user = Customer.objects.get(user=request.auth.user)

        if request.method == "DELETE":
            open_order = Order.objects.get(
                customer=current_user, payment_type=None)
            line_item = OrderProduct.objects.filter(
                product__id=int(request.data["product_id"]),
                order=open_order
            )[0]
            line_item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        if request.method == "GET":
            try:
                open_order = Order.objects.get(
                    customer=current_user, payment_type=None)
                products_on_order = Product.objects.filter(
                    cart__order=open_order)

                serialized_order = OrderSerializer(
                    open_order, many=False, context={'request': request})
                product_list = ProductSerializer(
                    products_on_order, many=True, context={'request': request})

                final = {
                    "order": serialized_order.data
                }
                final["order"]["products"] = product_list.data
                final["order"]["size"] = len(products_on_order)

            except Order.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            return Response(final)

        if request.method == "PUT":
            try:
                open_order = Order.objects.get(
                    customer=current_user, payment_type=None)
            except Order.DoesNotExist as ex:
                open_order = Order()
                open_order.created_date = datetime.datetime.now()
                open_order.customer = current_user
                open_order.save()

            line_item = OrderProduct()
            line_item.product = Product.objects.get(
                pk=request.data["product_id"])
            line_item.order = open_order
            line_item.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get', 'put', 'delete'], detail=False)
    def cart(self, request):
        """Shopping cart route for customers

        Returns:
            Response -- An HTTP response
        """
        current_user = Customer.objects.get(user=request.auth.user)

        if request.method == "DELETE":
            open_order = Order.objects.get(
                customer=current_user, payment_type=None)
            line_item = OrderProduct.objects.filter(
                product__id=int(request.data["product_id"]),
                order=open_order
            )[0]
            line_item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        if request.method == "GET":
            try:
                open_order = Order.objects.get(
                    customer=current_user, payment_type=None)
                products_on_order = Product.objects.filter(
                    cart__order=open_order)

                serialized_order = OrderSerializer(
                    open_order, many=False, context={'request': request})
                product_list = CartProductSerializer(
                    products_on_order, many=True, context={'request': request})

                final = {
                    "order": serialized_order.data
                }
                final["order"]["products"] = product_list.data
                final["order"]["size"] = len(products_on_order)

            except Order.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            return Response(final["order"])

        if request.method == "PUT":
            try:
                open_order = Order.objects.get(
                    customer=current_user, payment_type=None)
            except Order.DoesNotExist as ex:
                open_order = Order()
                open_order.created_date = datetime.datetime.now()
                open_order.customer = current_user
                open_order.save()

            line_item = OrderProduct()
            line_item.product = Product.objects.get(
                pk=request.data["product_id"])
            line_item.order = open_order
            line_item.save()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
