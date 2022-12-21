from rest_framework import (
    generics,
    status,
)

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer

class CreateUserView(APIView):
    """Create a new user and return new user's email and jwt_token"""

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            user = serializer.save()

            data.update(serializer.data)
            refresh = RefreshToken.for_user(user)
            data["jwt"] = {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)