from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .models import FriendRequest
from django.shortcuts import get_object_or_404
from .serializers import FriendSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        receiver = get_object_or_404(User, username=request.data['receiver_username'])
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
        return Response({'message': 'The request has been accepted'}, status=200)
        

class FriendsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        query = request.user.friends
        return Response({'data':FriendRequest(query, many=True).data,
                          'message': 'Friends have been found successfully'}, status=200)