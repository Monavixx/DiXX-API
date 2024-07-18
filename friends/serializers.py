from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import FriendRequest


class FriendSerializer (serializers.ModelSerializer):
    friendship = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.data_user = kwargs.pop('data_user', None)
        super().__init__(*args, **kwargs)

        if self.data_user is None:
            self.fields.pop('friendship')
    
    def get_friendship(self, obj):
        # 3: They are friends
        # 2: Request from him
        # 1: Request from me
        # 0: They aren't friends
        if self.data_user.friends.filter(pk=obj.pk).exists():
            return {'status':3}
        request_to_me = self.data_user.requests_to_me.filter(sender__pk=obj.pk)
        if request_to_me.exists():
            return {'status':2, 'request':FriendRequestSerializer(request_to_me.first()).data}
        request_from_me = self.data_user.requests_from_me.filter(receiver__pk=obj.pk)
        if request_from_me.exists():
            return {'status':1, 'request': FriendRequestSerializer(request_from_me.first()).data}
        return {'status':0}

    class Meta:
        model = User
        fields = ['username', 'id', 'friendship']
    

class FriendRequestSerializer (serializers.ModelSerializer):
    sender = FriendSerializer()
    class Meta:
        model = FriendRequest
        fields = ['sender', 'request_datetime', 'id']