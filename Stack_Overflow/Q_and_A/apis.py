from Q_and_A.models import Questions
from Q_and_A.serializers import AnswerSerializer, QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


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
        
        serializer = QuestionSerializer(data=data)
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