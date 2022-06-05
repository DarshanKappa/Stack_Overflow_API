from Q_and_A.models import Questions
from Q_and_A.serializers import AnswerSerializer, QuestionListSerializer, QuestionSerializer, QuestionsAnswerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from users.utils import pydantic_validation


class QuestionAPIView(APIView):
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
        
        return Response(data={'question': serializer.data})

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
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        data = request.data
        
        serializer = AnswerSerializer(data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors.get('non_field_errors'), status=400)
        serializer.save()

        return Response(data={'answer': serializer.data}, status=201)
    

class BaseLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100

class QuestionAnswerList(ListAPIView):
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    queryset = Questions.objects.all()
    serializer_class = QuestionsAnswerSerializer
    pagination_class = BaseLimitOffsetPagination
    
    
class QuestionsOfUser(ListAPIView):
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    serializer_class = QuestionListSerializer
    pagination_class = BaseLimitOffsetPagination

    def get(self, request, user_id, *args, **kwargs):
        self.queryset = Questions.objects.filter(user=user_id).order_by('-vote')
        resp = self.list(request, user_id, *args, **kwargs)
        return Response(data=resp.data)