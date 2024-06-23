from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import CardSerializer, SetSerializer, SetOverviewSerializer
from .models import Set, Card
import random

from django.contrib.auth import get_user_model
User = get_user_model()


class MySetViewSet(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request : Request):
        query = request.user.sets.all()
        return Response(SetOverviewSerializer(query, many=True).data)
    def handle_exception(self, exc):
        print(exc.detail)
        return Response({'message': exc.detail}, status=exc.status_code)

class SetView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, id):
        query = Set.objects.get(id=id)
        if query.is_private and request.user != query.author:
            return Response({'is_private':True, 'message': 'This set is private', 'success': False})
        data = SetOverviewSerializer(query).data
        data['success'] = True
        return Response(data)
    
class LearnRandomView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, id):
        curSet = Set.objects.get(id=id)
        if curSet.is_private and curSet.author != request.user:
            return Response({'is_private':True, 'message': 'This set is private', 'success': False})
        cards = curSet.card_set.all()
        randomCard = cards[random.randint(0, len(cards)-1)]
        return Response(CardSerializer(randomCard).data)
    