from rest_framework import serializers
from .models import Card, Set
from main.serializers import UserPublicSerializer, UserUsernameSerializer

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['first', 'second', 'create_datetime', 'cardset']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('cardset')
        return representation

class SetSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField('username', read_only=True)
    card_set = CardSerializer(many=True)
    class Meta:
        model = Set
        fields = ['id', 'name', 'description', 'author', 'create_datetime', 'card_set', 'is_private', 'numberOfCards']

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', [
            'id', 'name', 'description', 'author', 'create_datetime',
            'card_set', 'is_private', 'numberOfCards'
        ])
        super().__init__(*args, **kwargs)
        if fields is None:
            fields = [
                'id', 'name', 'description', 'author', 'create_datetime',
                'is_private', 'numberOfCards'
            ]
        
        if fields is not None:
            useless = set(self.fields.keys()) - set(fields)
            for field in useless:
                self.fields.pop(field)


class SetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['id', 'name', 'description', 'author', 'is_private']