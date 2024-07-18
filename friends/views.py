from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .models import FriendRequest
from django.shortcuts import get_object_or_404
from .serializers import FriendSerializer, FriendRequestSerializer
from django.contrib.auth import get_user_model
from django.db.models import F
User = get_user_model()


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        receiver = get_object_or_404(User, username=request.data['receiver_username'])
        if request.user.friends.filter(pk=receiver.pk).exists():
            return Response({'message': 'You are already friends'}, status=409)
        if request.user == receiver:
            return Response({'message': 'You can\'t send request to yourself'}, status=400)
        fr, create = FriendRequest.objects.get_or_create(sender=request.user, receiver=receiver)
        if create:
            return Response({'message': 'The request has been sent successfully'}, status=200)
        else:
            return Response({'message': 'The request has been already sent'}, status=200)


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        fr = get_object_or_404(FriendRequest, pk=request.data['request_id'])
        if fr.receiver != request.user:
            return Response({'message': 'You are not receiver of the request'}, status=403)
        request.user.friends.add(fr.sender)
        fr.delete()
        return Response({'message': 'The request has been accepted'}, status=200)
        

class FriendsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        query = request.user.friends
        return Response({'data':FriendSerializer(query, many=True).data,
                          'message': 'Friends have been found successfully'}, status=200)

class FriendRequestViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        return Response({'data': FriendRequestSerializer(request.user.requests_to_me, many=True).data,
                         'message': 'Friend requests have been found successfully'}, status=200)
    
class FindPeopleViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        query = request.query_params['username'].strip()
        people = User.objects \
            .filter(username__icontains=query) \
            .exclude(pk=request.user.pk) \
            .exclude(username='AnonymousUser')
        return Response({'data': FriendSerializer(people, many=True, data_user=request.user).data, 
                         'message': 'People have been found successfully'}, status=200)
    
class UnfriendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        friend = get_object_or_404(User, username=request.data['username'])
        if not request.user.friends.filter(pk=friend.pk).exists():
            return Response({'message': f'User \'{friend.username}\' is not your friend'}, status=400)
        request.user.friends.remove(friend)
        return Response({'message':f'User \'{friend.username}\' has been unfriended successfully'}, status=200)