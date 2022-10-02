from rest_framework import serializers

from community.models import Question, Answer


class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['contents']


class QuestionDetailSerializer(serializers.ModelSerializer):
    klass_title = serializers.ReadOnlyField(source='klass.title')
    student = serializers.ReadOnlyField(source='student.username')

    class Meta:
        model = Question
        fields = ['klass_title', 'student', 'contents']