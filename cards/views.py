from django.http import Http404
from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import CardSerializer, SetSerializer
from .models import Set, Card
import random
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
User = get_user_model()


class MySetsViewSet(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request : Request):
        query = request.user.sets.all()
        return Response(SetSerializer(query, many=True).data)


class SetView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id):
        query = Set.objects.get(id=id)

        if query.is_private and request.user != query.author:
            return Response({'is_private':True, 'message': 'This set is private.'}, status=403)
        
        #Client can choose what fields the server has to give him
        fields = request.query_params.get('fields').split(',') if 'fields' in request.query_params else None
        data = SetSerializer(query, fields=fields).data
        
        return Response(data)
    
    def handle_exception(self, exc):
        if isinstance(exc, Set.DoesNotExist):
            return Response({'message': 'The set with such an id was not found.'}, status=404)
        return super().handle_exception(exc)
    


class LearnRandomView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, id):
        curSet = Set.objects.get(id=id)
        if curSet.is_private and curSet.author != request.user:
            return Response({'is_private':True, 'message': 'This set is private', 'success': False})
        cards = curSet.card_set.all()
        randomCard = cards[random.randint(0, len(cards)-1)]
        return Response(CardSerializer(randomCard).data)
    

class CreateSetView(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request: Request):
        name = request.data.get('name')
        description = request.data.get('description')
        is_private = request.data.get('is_private')

        print(name, description, is_private)

        newSet = Set.objects.create(name=name, description=description,
                            is_private=is_private, author=request.user)
        
        newSet.users.add(request.user)

        return Response({'message': 'A new set was successfully created.'}, status=200)
    