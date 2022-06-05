from Q_and_A.pydantic import AnswerValidation, AnswerVoteValidation, QuestionValidation, QuestionVoteValidation
from rest_framework import serializers
from users.utils import pydantic_validation
from .models import AnswerUserVotes, Answers, QuestionUserVotes, Questions

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
        return data
    
    def validate(self, data):
        is_valid, msg = pydantic_validation(AnswerValidation, data)
        if not is_valid:
            raise serializers.ValidationError(msg)
        data.update({'question': data.pop('question_id')})
        return data
    
    def create(self, validate_data):
        request = self.context.get('request')
        validate_data.update({'user':request.user})
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
    
    
class VoteToQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = QuestionUserVotes
        fields = ['user', 'question', 'up_down_vote']
        
    def to_internal_value(self, data):
        return data
    
    def validate(self, data):
        is_valid, msg = pydantic_validation(QuestionVoteValidation, data)
        if not is_valid:
            raise serializers.ValidationError(msg)
        data.update({'question':data.pop('question_id')})
        return data
    
    def create(self, validate_data):
        request = self.context.get('request')
        validate_data.update({'user':request.user})
        question = Questions.objects.get(pk=int(validate_data.get('question')))
        validate_data.update({'question':question})
        instance = QuestionUserVotes.objects.filter(user=validate_data.get('user'), question=question).first()
        if instance:
            return self.update(instance, validate_data)

        question_vote = QuestionUserVotes(**validate_data)
        question_vote.save()
        question = Questions.objects.get(pk=question.id)
        question.vote = len(question.question_votes.filter(up_down_vote='UP')) - len(question.question_votes.filter(up_down_vote='DOWN'))
        question.save()
        return question_vote

    def update(self, instance, validate_data):
        if instance.up_down_vote == validate_data.get('up_down_vote'):
            return instance
        instance.up_down_vote = validate_data.get('up_down_vote')
        instance.save()
        question = Questions.objects.get(pk=instance.question.id)
        question.vote = len(question.question_votes.filter(up_down_vote='UP')) - len(question.question_votes.filter(up_down_vote='DOWN'))
        question.save()
        return instance
    
class VoteToAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerUserVotes
        fields = ['user', 'answer', 'up_down_vote']

    def to_internal_value(self, data):
        return data
    
    def validate(self, data):
        is_valid, msg = pydantic_validation(AnswerVoteValidation, data)
        if not is_valid:
            raise serializers.ValidationError(msg)
        data.update({'answer':data.pop('answer_id')})
        return data
    
    def create(self, validate_data):
        request = self.context.get('request')
        validate_data.update({'user':request.user})
        answer = Answers.objects.get(pk=int(validate_data.get('answer')))
        validate_data.update({'answer':answer})
        instance = AnswerUserVotes.objects.filter(user=validate_data.get('user'), answer=answer).first()
        if instance:
            return self.update(instance, validate_data)

        answer_vote = AnswerUserVotes(**validate_data)
        answer_vote.save()
        answer = Answers.objects.get(pk=answer.id)
        answer.vote = len(answer.answer_votes.filter(up_down_vote='UP')) - len(answer.answer_votes.filter(up_down_vote='DOWN'))
        answer.save()
        return answer_vote

    def update(self, instance, validate_data):
        if instance.up_down_vote == validate_data.get('up_down_vote'):
            return instance
        instance.up_down_vote = validate_data.get('up_down_vote')
        instance.save()
        answer = Answers.objects.get(pk=instance.answer.id)
        answer.vote = len(answer.answer_votes.filter(up_down_vote='UP')) - len(answer.answer_votes.filter(up_down_vote='DOWN'))
        answer.save()
        return instance