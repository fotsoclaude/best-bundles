from rest_framework import serializers

from api.models import UserChoices


class UserChoicesSerializer(serializers.ModelSerializer):
    model = UserChoices

    amount = serializers.IntegerField()
    sms = serializers.IntegerField()
    call = serializers.IntegerField()
    datas = serializers.IntegerField()

    class Meta:
        model = UserChoices
        field = "__all__"
        extra_kwargs = {
            'amount': {'required': True, },
            'sms': {'required': True, },
            'call': {'required': True, },
            'datas': {'required': True, },
        }
