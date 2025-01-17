from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import viewsets, response, status, permissions
from .serializers import CreateContentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class ContentViewset(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        request_body=CreateContentSerializer,
        responses={201: CreateContentSerializer, 400: 'Bad Request'}
    )
    def create(self, request):
        serialiser = CreateContentSerializer(data=request.data, context={'request': request})
        if serialiser.is_valid():
            serialiser.save()
            return response.Response(serialiser.data, status=status.HTTP_201_CREATED)
        return response.Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)

        

