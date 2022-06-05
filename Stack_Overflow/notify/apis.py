from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Notify
from .serializers import QuestionersAnswersNotificationSerilizer


class AnswerNotification(ListAPIView):
    '''
    Notify when reply on the question. This API Return instance only one time
    Like notification
    '''
    authentication_classes = [JWTAuthentication,]
    permission_classes = [IsAuthenticated]
    
    serializer_class = QuestionersAnswersNotificationSerilizer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Notify.objects.filter(user=user, user_type='Q')
        return queryset
    
    def get(self, request, *args, **kwargs):
        resp = self.list(request, *args, **kwargs)
        queryset = self.get_queryset()
        queryset.delete()
        return Response(resp.data)
    
class ApprovedNotification(AnswerNotification):
    '''
    Notify when approve the answer by questioner. This API Return instance only one time
    Like notification
    '''
    
    def get_queryset(self):
        user = self.request.user
        queryset = Notify.objects.filter(user=user, user_type='A')
        return queryset