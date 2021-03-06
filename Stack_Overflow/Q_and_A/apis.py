from Q_and_A.models import Answers, Questions
from Q_and_A.pydantic import AnswerApprovalVlaidation
from Q_and_A.serializers import VoteToAnswerSerializer, AnswerSerializer, QuestionSerializer, QuestionsAnswerSerializer, VoteToQuestionSerializer
from notify.models import Notify
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from users.utils import pydantic_validation
from django.contrib.auth.models import User


class QuestionAPIView(APIView):
    '''
    API to Crate, Update and Retrive the Question
    '''
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id, *args, **kwargs):
        
        question = Questions.objects.filter(pk=id).first()
        if not question:
            return Response("Invalid question id", status=400)
        serializer = QuestionSerializer(question)
        
        return Response(data={'question': serializer.data})
    
    def post(self, request, *args, **kwargs):
        data = request.data
        
        serializer = QuestionSerializer(data=data, context={'request':request})
        if not serializer.is_valid():
            return Response(data=serializer.errors.get('non_field_errors'), status=400)
        serializer.save()
        
        return Response(data={'question': serializer.data}, status=201)

    def put(self, request, id, *args, **kwargs):
        data = request.data
        
        question = Questions.objects.filter(pk=id).first()
        if not question:
            return Response("Invalid question id", status=400)
        
        serializer = QuestionSerializer(question, data)
        if not serializer.is_valid():
            return Response(data=serializer.errors.get('non_field_errors'), status=400)
        serializer.save()

        return Response(data={'question':serializer.data})
    
    
class AnswerAPIView(APIView):
    '''
    API to Create Answer on any Question
    '''
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        data = request.data
        
        serializer = AnswerSerializer(data=data, context={'request':request})
        if not serializer.is_valid():
            return Response(data=serializer.errors.get('non_field_errors'), status=400)
        answer = serializer.save()

        # add notification to notify to questioner
        notification = Notify(user=answer.question.user, user_type='Q', question=answer.question, answer=answer)
        notification.save()

        return Response(data={'answer': serializer.data}, status=201)
    

class BaseLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100

class QuestionAnswerList(ListAPIView):
    '''
    Return List of All Questions with those Answers
    '''
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    queryset = Questions.objects.all()
    serializer_class = QuestionsAnswerSerializer
    pagination_class = BaseLimitOffsetPagination
    
    
class QuestionsOfUser(ListAPIView):
    '''
    Return List of Questions with those Answers which create by authanticated user
    '''
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    serializer_class = QuestionsAnswerSerializer
    pagination_class = BaseLimitOffsetPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Questions.objects.filter(user=user)
        return queryset


class AnswerApproval(APIView):
    '''
    API to approve answer by questioner
    '''
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        
        is_valid, msg = pydantic_validation(AnswerApprovalVlaidation, data)
        if not is_valid:
            return Response(msg, status=400)
        
        answer = Answers.objects.get(pk=data.get('answer_id'))
        if user != answer.question.user:
            return Response("Invalid answer id", status=400)

        if answer.is_approved == True:
            return Response({})

        answer.is_approved = True
        answer.save()
        
        # add Notification to notify to Answerer whos answer approved by Questioner
        notification = Notify(user=answer.user , user_type='A', question=answer.question, answer=answer)
        notification.save()
        
        return Response({})
        

class SearchQuestions(ListAPIView):
    '''
    Enter tag and return question accordign tag
    '''
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    serializer_class = QuestionsAnswerSerializer
    pagination_class = BaseLimitOffsetPagination
    
    def get_queryset(self):
        tag = self.request.query_params.get('tag')
        queryset = Questions.objects.filter(tag=tag)
        return queryset
    
    
class VoteToQuestion(APIView):
    '''
    API to give Vote to questions
    '''
    
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = VoteToQuestionSerializer(data=data, context={'request':request})
        if not serializer.is_valid():
            return Response(data=serializer.errors.get('non_field_errors'), status=400)
        serializer.save()

        return Response(data={})
    
class VoteToAnswer(APIView):
    '''
    API to give Vote to Answer
    '''
    
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = VoteToAnswerSerializer(data=data, context={'request':request})
        if not serializer.is_valid():
            return Response(data=serializer.errors.get('non_field_errors'), status=400)
        serializer.save()

        return Response(data={})

