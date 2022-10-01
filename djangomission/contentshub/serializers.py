from accounts.models import User
from contentshub.models import Klass
from rest_framework import serializers

class KlassCreateSerializer(serializers.ModelSerializer):
    master = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Klass
        fields = ['master', 'title', 'description'] 