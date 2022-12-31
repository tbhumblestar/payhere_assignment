from rest_framework import (
    generics,
    status,
)

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from user.serializers import UserSerializer, CustomTokenObtainPairTokenSerializer


class CreateUserView(APIView):
    """Create a new user and return new user's email and jwt_token"""

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            data["access"] = str(refresh.access_token)
            data["refresh"] = str(refresh)
            data.update(serializer.data)

            return Response(data, status=status.HTTP_201_CREATED)
        
        else:
            data = serializer.errors
            
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



class ObtainPairTokenView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairTokenSerializer