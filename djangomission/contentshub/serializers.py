from rest_framework import serializers

from .models import Master, Klass


class SetMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Master
        fields = ['master_name', 'description']


class KlassCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Klass
        fields = ['title', 'description']


class KlassDetailSerializer(serializers.ModelSerializer):
    master_name = serializers.ReadOnlyField(source='master.master_name')

    class Meta:
        model = Klass
        fields = ['master', 'master_name', 'title', 'description']
