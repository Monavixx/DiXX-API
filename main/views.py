from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import views, response, status, permissions
from django.contrib.auth import authenticate, login, logout, get_user_model
from .serializers import UserPublicSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

User = get_user_model()


import logging

logger = logging.getLogger("mylogger")

def information_about_api(request):
    return JsonResponse({'version':'0.0.1'})

class LoginView(views.APIView):
    def _error_response(self, message):
        return Response({
            'message': message
        }, status=400)
    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is None:
            return self._error_response('invalid')
        if not user.is_active:
            return self._error_response('disabled')
        
        login(request, user)
        
        data = UserPublicSerializer(request.user).data
        return Response({'data':data, 'message': 'successful authentication!'}, status=200)

    def get(self, request: Request):
        if request.user is None or not request.user.is_authenticated:
            return Response({'message': 'not authenticated'}, status=401)
        data = UserPublicSerializer(request.user).data
        return Response({'data':data, 'message': 'You are logged in'}, status=200)


class LogoutView(views.APIView):
    def get(self, request: Request):
        logout(request)
        return Response({'message': 'Successful logout.'}, status=200)


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