from .serializers import UserSignupSerializer
from rest_framework.response import Response
from rest_framework import viewsets, status

class SignupViewset(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


