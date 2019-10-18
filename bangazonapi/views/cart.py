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
from .order import OrderSerializer


class Cart(ViewSet):
    """Shopping cart for Bangazon eCommerce"""

    def create(self, request):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
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


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        current_user = Customer.objects.get(user=request.auth.user)
        open_order = Order.objects.get(
            customer=current_user, payment_type=None)
        line_item = OrderProduct.objects.filter(
            product__id=int(request.data["product_id"]),
            order=open_order
        )[0]
        line_item.delete()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
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
            final["order"]["size"] = len(products_on_order)

        except Order.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        return Response(final.values())
