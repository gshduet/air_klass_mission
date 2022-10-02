from rest_framework import serializers

from .models import Master
from accounts.models import User


class SetMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Master
        fields = (
            'master_name',
            'description'
        )

