from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import CardSerializer, SetSerializer, SetOverviewSerializer
from .models import Set, Card

from django.contrib.auth import get_user_model
User = get_user_model()

import logging
logger = logging.getLogger("rgrgrg")


class SetViewSet(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request : Request):
        query = request.user.sets.filter(author=request.user)
        return Response(SetOverviewSerializer(query, many=True).data)

class SetView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request: Request, id):
        query = Set.objects.get(id=id)
        return Response(SetSerializer(query).data)