"""
   Author: Daniel Krusch
   Purpose: To convert product category data to json
   Methods: GET, POST
"""

"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from bangazonapi.models import ProductCategory
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProductCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = ProductCategory
        fields = ('id', 'name')


class ProductCategories(ViewSet):
    """Park Areas for Kennywood Amusement Park"""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized product category instance
        """
        new_product_category = ProductCategory()
        new_product_category.name = request.data["name"]
        new_product_category.save()

        serializer = ProductCategorySerializer(new_product_category, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            category = ProductCategory.objects.get(pk=pk)
            serializer = ProductCategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to park ProductCategorys resource

        Returns:
            Response -- JSON serialized list of park ProductCategorys
        """
        product_category = ProductCategory.objects.all()

        # Support filtering ProductCategorys by area id
        # name = self.request.query_params.get('name', None)
        # if name is not None:
        #     ProductCategories = ProductCategories.filter(name=name)

        serializer = ProductCategorySerializer(
            product_category, many=True, context={'request': request})
        return Response(serializer.data)
