from Q_and_A.models import Answers, Questions
from Q_and_A.serializers import AnswerListSerializer, QuestionListSerializer
from rest_framework import serializers


class QuestionersAnswersNotificationSerilizer(serializers.Serializer):
    
    question = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    
    class Meta:
        fields = [
            'question',
            'answer',
        ]
        
    def get_question(self, obj):
        queryset = Questions.objects.get(pk=obj.question.id)
        return QuestionListSerializer(queryset).data
    
    def get_answers(self, obj):
        queryset = Answers.objects.get(pk=obj.answer.id)
        return AnswerListSerializer(queryset).data
    
        
    