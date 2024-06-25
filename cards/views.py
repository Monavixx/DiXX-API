from django.http import Http404
from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import CardSerializer, SetCreateSerializer, SetSerializer
from .models import Set, Card
import random
from django.shortcuts import get_object_or_404

from django.contrib.auth import get_user_model
User = get_user_model()


class MySetsViewSet(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request : Request):
        query = request.user.sets.all()
        return Response({'data':SetSerializer(query, many=True).data, 'message':'Your sets have been found successfully.'})


class SetView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id):
        query = Set.objects.get(id=id)

        if query.is_private and request.user != query.author:
            return Response({'data':{'is_private':True}, 'message': 'This set is private.'}, status=403)
        
        #Client can choose what fields the server has to give him
        fields = request.query_params.get('fields').split(',') if 'fields' in request.query_params else None
        data = SetSerializer(query, fields=fields).data
        
        return Response({'data':data, 'message': 'Set has been found successfully.'})
    
    def handle_exception(self, exc):
        if isinstance(exc, Set.DoesNotExist):
            return Response({'message': 'The set with such an id was not found.'}, status=404)
        return super().handle_exception(exc)
    


class LearnRandomView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id):
        curSet = Set.objects.get(id=id)
        if curSet.is_private and curSet.author != request.user:
            return Response({'message': 'This set is private', 'success': False}, status=403)
        cards = curSet.card_set.all()
        if len(cards) <= 0:
            return Response({'message': 'There aren\'t any cards in this set.'}, status=404)
        randomCard = cards[random.randint(0, len(cards)-1)]
        return Response({'data':CardSerializer(randomCard).data, 'message':'Random card has been found successfully.'})
    

class CreateSetView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = SetCreateSerializer(data=data)
        if serializer.is_valid():
            serializer.save().users.add(request.user)
            return Response({'data':serializer.data, 
                             'message': 'Set has been created successfully'}, status=201)
        return Response({'errors':serializer.errors, 'message': 'Failed to create set'}, status=400)


class RemoveSetView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        set_id = request.data.get('set_id')
        Set.objects.get(id=set_id).users.remove(request.user)
        return Response({'message': 'The set was successfully removed.'}, status=200)


class EditSetView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Set, pk=pk)
    
    def put(self, request, pk):
        set_instance = self.get_object(pk)
        if request.user == set_instance.author:
            serializer = SetSerializer(set_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Set has been changed successfully.'}, status=204)
            else:
                return Response({'errors': serializer.errors, 'message': 'Failed to edit set.'}, status=400)
        else:
            return Response({'message': 'You aren\'t the author of this set.'}, status=403)
        


class AddCardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk):
        if Set.objects.get(pk=pk).author != request.user:
            return Response({'message': 'You aren\'t the author of this set.'}, status=403)
        serializer = CardSerializer(data=request.data)
        serializer.initial_data['cardset'] = pk
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Card has been added successfully'}, status=201)
        return Response({'errors': serializer.errors, 'message': 'Failed to add card.'}, status=400)