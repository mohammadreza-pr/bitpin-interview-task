from drf_yasg.utils import swagger_auto_schema 
from drf_yasg import openapi
from .models import Content
from rest_framework import viewsets, response, status, permissions
from .serializers import CreateContentSerializer, ContentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination


class ContentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ContentViewset(viewsets.ViewSet):

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ContentPagination

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
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description='Page number for pagination',
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ]
    )
    def list(self, request):
        queryset = Content.objects.all().order_by('-created_at')  
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ContentSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

        

