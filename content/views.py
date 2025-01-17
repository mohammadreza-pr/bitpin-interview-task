from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_yasg import openapi
from .models import Content
from confluent_kafka import Producer
from rest_framework import viewsets, response, status, permissions
from .serializers import CreateContentSerializer, ContentSerializer, RateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
import json


class ContentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ContentViewset(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]
    pagination_class = ContentPagination

    @extend_schema(
        request=CreateContentSerializer,
        responses={201: CreateContentSerializer, 400: 'Bad Request'}
    )
    def create(self, request):
        serialiser = CreateContentSerializer(data=request.data, context={'request': request})
        if serialiser.is_valid():
            serialiser.save()
            return response.Response(serialiser.data, status=status.HTTP_201_CREATED)
        return response.Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='page',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Page number for pagination',
                required=False,
            ),
        ]
    )
    def list(self, request):
        queryset = Content.objects.all().order_by('-created_at')  
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = ContentSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

class RateViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def send_to_kafka(self, topic, message):
        conf = {'bootstrap.servers': settings.KAFKA_BROKER_URL}
        producer = Producer(**conf)
        try:
            producer.produce(topic, json.dumps(message).encode('utf-8'))
            producer.flush()
            print(f"Message sent to topic '{topic}': {message}")
        except Exception as e:
            print(f"Error producing to Kafka: {e}")

    @extend_schema(
        request=RateSerializer,
        responses={202: RateSerializer, 400: 'Bad Request'}
    )
    def create(self, request):
        serializer = RateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            message = {
                "user_id": request.user.id,
                "post_id": serializer.validated_data['post'].id,
                "score": serializer.validated_data['score'],
                "weight": 1,
            }
            self.send_to_kafka(settings.KAFKA_TOPIC_RATINGS, message)
            return response.Response(
                {"message": "Rating has been subscribed."}, 
                status=status.HTTP_202_ACCEPTED
            )
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
