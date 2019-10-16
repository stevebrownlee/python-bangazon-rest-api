from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Customer


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for customers
    Author: Dustin Hobson

    Arguments:
        serializers
    """
    # Depth of one allows user object to be seen on Customer
    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='customer',
            lookup_field='id'

        )
        fields = ('id', 'url', 'user', 'phone_number', 'address')
        depth = 1


class Customers(ViewSet):
    """Customers for Bangazon
    Author: Dustin Hobson
    Purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE Customers.
    Methods: GET PUT(id) POST
    """
    def update(self, request, pk=None):
        customer = Customer.objects.get(pk=pk)
        customer.user.is_active = False
        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
