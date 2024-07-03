from django.http import Http404
from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import CardSerializer, SetCreateSerializer, SetSerializer
from .models import Set, Card
import random
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from guardian.shortcuts import assign_perm, get_objects_for_user

from django.contrib.auth import get_user_model
User = get_user_model()


class MySetsViewSet(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request : Request):
        query = get_objects_for_user(request.user, 'set_view', request.user.sets.all().order_by('-create_datetime'))
        serializer = SetSerializer(query, many=True, fields=None)
        data = serializer.data
        return Response({'data':data, 'message':'Your sets have been found successfully.'})


class SetView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id):
        query = Set.objects.get(id=id)

        if query.is_private and not request.user.has_perm('set_view', query):
            return Response({'data':{'is_private':True}, 'message': 'This set is private.'}, status=403)
        
        #Client can choose what fields the server has to give him
        fields = request.query_params.get('fields').split(',') \
            if ('fields' in request.query_params and len(request.query_params['fields']) > 0) else None
        data = SetSerializer(query, fields=fields).data.copy()
        data['is_your_one'] = query.users.contains(request.user)

        
        return Response({'data':data, 'message': 'Set has been found successfully.'})
    
    def handle_exception(self, exc):
        if isinstance(exc, Set.DoesNotExist):
            return Response({'message': 'The set with such an id was not found.'}, status=404)
        return super().handle_exception(exc)
    


class LearnRandomView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id):
        curSet = Set.objects.get(id=id)
        if curSet.is_private and not request.user.has_perm('set_view', curSet):
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
            newSet = serializer.save()
            newSet.users.add(request.user)

            assign_perm('set_edit', request.user, newSet)
            assign_perm('set_delete', request.user, newSet)
            assign_perm('set_view', request.user, newSet)

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
        set_instance = self.get_object(pk=pk)
        if request.user.has_perm('set_edit', set_instance):
            serializer = SetSerializer(set_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Set has been changed successfully.'}, status=204)
            else:
                return Response({'errors': serializer.errors, 'message': 'Failed to edit set.'}, status=400)
        else:
            return Response({'message': 'You can\'t edit this set.'}, status=403)


class AddCardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk):
        if not request.user.has_perm('set_edit', Set.objects.get(pk=pk)):
            return Response({'message': 'You can\'t add cards to this set.'}, status=403)
        serializer = CardSerializer(data=request.data)
        serializer.initial_data['cardset'] = pk
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'message': 'Card has been added successfully'}, status=201)
        return Response({'errors': serializer.errors, 'message': 'Failed to add card.'}, status=400)
    
class DeleteCardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        pk = request.data.get('id')
        try:
            card = Card.objects.get(pk=pk)
            if not request.user.has_perm('set_edit', card.cardset):
                return Response({'message': 'You can\'t delete card from this set.'}, status=403)
            card.delete()
            return Response({'message': 'Card has been deleted successfully.'}, status=200)
        except Card.DoesNotExist:
            return Response({'message':'Card hasn\'t been found.'}, status=404)

class AddSetView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        pk = request.data.get('id')
        cardset = Set.objects.get(pk=pk)
        if cardset.is_private and not request.user.has_perm('set_view', cardset):
            return Response({'message': 'You can\'t add the private set'}, status=403)
        cardset.users.add(request.user)
        return Response({'message':'You added this set successfully.'}, status=200)
