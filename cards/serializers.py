from rest_framework import serializers
from .models import Card, Set
from main.serializers import UserPublicSerializer, UserUsernameSerializer

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['first', 'second', 'create_datetime']

class SetSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField('username', read_only=True)
    card_set = CardSerializer(many=True)
    class Meta:
        model = Set
        fields = ['id', 'name', 'description', 'author', 'create_datetime', 'card_set', 'is_private']
class SetOverviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField('username', read_only=True)
    class Meta:
        model = Set
        fields = ['id', 'name', 'description', 'author', 'create_datetime', 'is_private']