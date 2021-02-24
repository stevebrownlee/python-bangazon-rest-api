"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import Payment, Customer

'''
auther: Tyler Carpenter
purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE entries.
methods: all
'''


class PaymentSerializer(serializers.ModelSerializer):
    """JSON serializer for Payment

    Arguments:
        serializers
    """
    class Meta:
        model = Payment
        fields = ('id', 'merchant_name', 'account_number', 'expiration_date', 'create_date')


class Payments(ViewSet):


    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized payment instance
        """
        new_payment = Payment()
        new_payment.merchant_name = request.data["merchant_name"]
        new_payment.account_number = request.data["account_number"]
        new_payment.expiration_date = request.data["expiration_date"]
        new_payment.create_date = request.data["create_date"]
        customer = Customer.objects.get(user=request.auth.user)
        new_payment.customer = customer
        new_payment.save()

        serializer = PaymentSerializer(new_payment, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single payment type

        Returns:
            Response -- JSON serialized payment_type instance
        """
        try:
            payment_type = Payment.objects.get(pk=pk)
            serializer = PaymentSerializer(payment_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park are

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Payment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
            Response -- JSON serialized list of park attractions
        """
        payment_types = Payment.objects.all()

        # Support filtering attractions by area id
        payment_type = self.request.query_params.get('customer', None)
        if payment_type is not None:
            payment_types = payment_types.filter(customer__id=payment_type)

        serializer = PaymentSerializer(
            payment_types, many=True, context={'request': request})
        return Response(serializer.data)