

from rest_framework import serializers

from payment.models import MomoRequest
from django.contrib.auth.models import User


class MomoRequestSerializer(serializers.Serializer):
    '''
    New momo request serializer
    '''
    amount = serializers.DecimalField(max_digits=5, decimal_places=3)
    user_requested_for = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super(MomoRequestSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):

        errmsg = {}  # Since raise forms.ValidationError causes immediate termination

        user_id = data.get('user_requested_for', 0)
        amount = data.get('amount', 0)

        if not user_id or not User.objects.filter(pk=user_id, is_active=1).exists():
            errmsg['user_requested_for'] = 'User to send the payment request to does not exist'

        amount = float(amount)
        if amount <= 0:
            errmsg['amount'] = 'Amount must be greater than zero'
        else:
            # we dont want to convert it again
            data['amount'] = amount

        if errmsg:
            raise serializers.ValidationError(errmsg)

        return data
