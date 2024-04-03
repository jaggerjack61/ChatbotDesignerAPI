from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import UserSerializer


class ObtainAuthToken(APIView):
    permission_classes = []  # Allow unauthenticated requests

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=400)

        try:
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'Invalid credentials'}, status=400)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Or filter as needed
    serializer_class = UserSerializer
