"""
   Author: Daniel Krusch
   Purpose: To convert order products data to json
   Methods: GET, DELETE, POST
"""

"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import OrderProduct, Order, Product


class LineItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = OrderProduct
        url = serializers.HyperlinkedIdentityField(
            view_name='orderproduct',
            lookup_field='id'
        )
        fields = ('id', 'url', 'order', 'product')

class LineItems(ViewSet):
    """Line items for Bangazon orders"""

    def retrieve(self, request, pk=None):
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            serializer = LineItemSerializer(order_product, context={'request': request})
            return Response(serializer.data)
        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single line item

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            order_product = OrderProduct.objects.get(pk=pk)
            order_product.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except OrderProduct.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
