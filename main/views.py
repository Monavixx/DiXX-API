from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import views, response, status, permissions
from django.contrib.auth import authenticate, login, logout
from .serializers import UserEmailAndNameSerializer
from rest_framework.response import Response
from rest_framework.request import Request
from django.contrib.auth.models import User

import logging

logger = logging.getLogger("mylogger")

def information_about_api(request):
    return JsonResponse({'version':'0.0.1'})

class LoginView(views.APIView):
    def _error_response(self, message):
        return Response({
            'is_authenticated': False,
            'message': message
        })
    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is None:
            return self._error_response('invalid')
        if not user.is_active:
            return self._error_response('disabled')
        
        login(request, user)
        
        data = UserEmailAndNameSerializer(request.user).data
        data['is_authenticated'] = True
        data['message'] = 'successful authentication!'
        return Response(data)

    def get(self, request: Request):
        if request.user is None or not request.user.is_authenticated:
            return self._error_response('not authenticated')
        data = UserEmailAndNameSerializer(request.user).data
        data['is_authenticated'] = True
        data['message'] = 'You are already logged in'
        return Response(data)


class LogoutView(views.APIView):
    def get(self, request: Request):
        logout(request)
        return Response({'message':'successful logout'})