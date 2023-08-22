from rest_framework import serializers
from .models import Deal


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    spent_money = serializers.IntegerField()
    gems = serializers.CharField(max_length=256)
