from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from Q_and_A.apis import BaseLimitOffsetPagination
from .models import Notify
from .serializers import QuestionersAnswersNotificationSerilizer
from django.contrib.auth.models import User

class ListNotification(ListAPIView):
    authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsAuthenticated]
    
    serializer_class = QuestionersAnswersNotificationSerilizer
    pagination_class = BaseLimitOffsetPagination
    
    def get_queryset(self):
        user = self.request.user
        queryset = Notify.objects.filter(user=User.objects.get(pk=1), user_type='Q')
        return queryset
    
    