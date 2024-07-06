from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import views
from django.contrib.auth import authenticate, logout, get_user_model
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


def information_about_api(request):
    return JsonResponse({'version':'0.0.1'})

class LoginView(views.APIView):
    def _error_response_400(self, message):
        return Response({
            'message': message
        }, status=400)
    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is None:
            return self._error_response_400('Invalid credentials')
        if not user.is_active:
            return self._error_response_400('User is disabled')
        
        token, created = Token.objects.get_or_create(user=user)

        data = UserSerializer(user).data
        data['token'] = token.key
        return Response({'data':data, 'message': 'Successful authentication'}, status=200)

    def get(self, request: Request):
        if request.user is None:
            return Response({'message': 'Unauthorized'}, status=401)
        data = UserSerializer(request.user).data
        return Response({'data':data, 'message': 'You are logged in'}, status=200)


class RegenerateTokenView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request):
        Token.objects.get(user=request.user).delete()
        token, created = Token.objects.get_or_create(user=request.user)

        return Response({'data': {'token': token},'message': 'Successful regenerate token.'}, status=200)


class RegistrationView(views.APIView):
    def post(self, request: Request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            User.objects.create_user(username=username, email=email, password=password)
        except ValidationError as e:
            return Response({'message':str(e.messages)}, status=400)
        except IntegrityError as e:
            return Response({'message':str(e.args)}, status=400)
        return Response({'message': 'successful registration'}, status=201)