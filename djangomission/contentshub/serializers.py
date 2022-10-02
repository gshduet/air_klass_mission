from rest_framework import serializers

from .models import Master, Klass
from accounts.models import User


class SetMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Master
        fields = (
            'master_name',
            'description'
        )


class KlassCreateSerializer(serializers.ModelSerializer):
    master = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Klass
        fields = ['master', 'title', 'description'] 


