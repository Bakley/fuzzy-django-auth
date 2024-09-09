from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import RegistrationSerializer, LoginSerializer
from .renderers import UserJSONRenderer

class RegistrationAPIView(GenericAPIView):
    """
    Register a new user
    """
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        data = request.data

        ser = self.serializer_class(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()


        return Response(
            ser.data,
            status=status.HTTP_201_CREATED
        )
    

class LoginAPIView(APIView):

    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        ser = self.serializer_class(data=user)
        ser.is_valid(raise_exception=True)

        return Response(
            ser.data,
            status=status.HTTP_200_OK
        )
