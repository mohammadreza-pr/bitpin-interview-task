from drf_spectacular.utils import extend_schema
from .serializers import UserSignupSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status

class SignupViewset(viewsets.ViewSet):
    @extend_schema(
        request=UserSignupSerializer,
        responses={201: UserSignupSerializer, 400: 'Bad Request'}
    )
    def create(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


