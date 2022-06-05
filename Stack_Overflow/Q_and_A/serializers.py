from re import A
from Q_and_A.pydantic import AnswerValidation, QuestionValidation
from rest_framework import serializers
from users.utils import pydantic_validation
from .models import Answers, Questions

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Questions
        fields = [
            'id',
            'user',
            'title',
            'body',
            'tag',
            'vote',
        ]

    def to_internal_value(self, data):
        return data
    
    def validate(self, data):
        is_valid, msg = pydantic_validation(QuestionValidation, data)
        if not is_valid:
            raise serializers.ValidationError(msg)
        return data
    
    def create(self, validate_data):
        request = self.context.get('request')
        validate_data.update({'user':request.user})
        question = Questions(**validate_data)
        question.save()
        return question
    
    def update(self, question, validate_data):
        question.title = validate_data.get('title')
        question.body = validate_data.get('body')
        question.tag = validate_data.get('tag')
        question.save()
        return question
    
    
class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answers
        fields = [
            'id',
            'question',
            'body',
        ]
        
    def to_internal_value(self, data):
        data.update({'question': data.pop('question_id')})
        return data
    
    def validate(self, data):
        is_valid, msg = pydantic_validation(AnswerValidation, data)
        if not is_valid:
            raise serializers.ValidationError(msg)
        return data
    
    def create(self, validate_data):
        question = Questions.objects.get(pk=int(validate_data.get('question')))
        validate_data.update({'question':question})
        answer = Answers(**validate_data)
        answer.save()
        return answer


class QuestionListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Questions
        fields = "__all__"

class AnswerListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answers
        fields = "__all__"

class QuestionsAnswerSerializer(serializers.Serializer):
    
    question = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    
    class Meta:
        fields = [
            'question',
            'answers',
        ]
        
    def get_question(self, obj):
        return QuestionListSerializer(obj).data
    
    def get_answers(self, obj):
        queryset = Answers.objects.filter(question=obj).order_by('-vote')
        return AnswerListSerializer(queryset, many=True).data