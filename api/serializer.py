from rest_framework import serializers

from api.models import UserChoices


class UserChoicesSerializer(serializers.ModelSerializer):
    amount = serializers.IntegerField()
    sms = serializers.IntegerField()
    call = serializers.IntegerField()
    data = serializers.IntegerField()
    validity = serializers.IntegerField()

    class Meta:
        model = UserChoices
        fields = "__all__"
        extra_kwargs = {
            'amount': {'required': True, },
            'sms': {'required': True, },
            'call': {'required': True, },
            'data': {'required': True, },
            'validity': {'required': True, },
        }

        def create(self, validate_data):
            user_choice = UserChoices.objects.create(
                amount=validate_data['amount'],
                sms=validate_data['sms'],
                call=validate_data['call'],
                datas=validate_data['datas'],
                validity=validate_data['validity']
            )
            user_choice.save()
            return user_choice
