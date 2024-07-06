from rest_framework import serializers
from .models import Card, Set
from main.serializers import UserPublicSerializer, UserUsernameSerializer

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'first', 'second', 'create_datetime', 'cardset']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('cardset')
        return representation

class SetSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField('username', read_only=True)
    card_set = CardSerializer(many=True)
    visibility_choices = serializers.SerializerMethodField()

    class Meta:
        model = Set
        fields = ['id', 'name', 'description', 'author', 'create_datetime',
                   'card_set', 'visibility', 'numberOfCards', 'visibility_choices']

    def __init__(self, *args, **kwargs):
        #fields = kwargs.pop('fields', [
        #    'id', 'name', 'description', 'author', 'create_datetime',
        #    'card_set', 'visibility', 'numberOfCards', 'visibility_choices'
        #])
        fields = kwargs.pop('fields', SetSerializer.Meta.fields)
        super().__init__(*args, **kwargs)
        if fields is None:
            fields = [
                'id', 'name', 'description', 'author', 'create_datetime',
                'visibility', 'numberOfCards'
            ]
        
        if fields is not None:
            useless = set(self.fields.keys()) - set(fields)
            for field in useless:
                self.fields.pop(field)

    def get_visibility_choices(self, obj):
        return Set.VISIBILITY_CHOICES


class SetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = ['id', 'name', 'description', 'author', 'visibility']