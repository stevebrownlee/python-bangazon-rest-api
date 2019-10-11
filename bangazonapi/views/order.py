"""View module for handling requests about park areas"""
import datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from bangazonapi.models import Order, Payment, Customer, Product, OrderProduct
from .product import ProductSerializer

'''
auther: Tyler Carpenter
purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE entries.
methods: all
'''


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order

    Arguments:
        serializers
    """

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'url', 'created_date', 'payment_type', "customer")


class Orders(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ParkArea instance
        """
        neworder = Order()
        neworder.created_date = request.data["created_date"]
        customer = Customer.objects.get(id=request.data["customer_id"])
        neworder.customer = customer
        neworder.save()

        serializer = OrderSerializer(neworder, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for order

        Returns:
            Response -- JSON serialized order
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        order = Order.objects.get(pk=pk)
        order.payment_type = request.data["payment_type"]
        order.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order = Order.objects.get(pk=pk)
            order.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        orders = Order.objects.all()

        customer = self.request.query_params.get('customer_id', None)
        payment = self.request.query_params.get('payment_id', None)
        if customer is not None:
            orders = orders.filter(customer__id=customer)
            if payment is None:
                orders = orders.filter(payment_type__id=None)
        if payment is not None:
            orders = orders.filter(payment__id=payment)

        serializer = OrderSerializer(
            orders, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get', 'put'], detail=False)
    def cart(self, request):
        """Shopping cart route for customers

        Returns:
            Response -- An HTTP response
        """
        if request.method == "GET":
            current_user = Customer.objects.get(user=request.auth.user)

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

            except Order.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            return Response(final)

        if request.method == "PUT":
            current_user = Customer.objects.get(user=request.auth.user)

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
