import json
from rest_framework.response import Response
from rest_framework.views import APIView
from users.pydentic import RegistrationValidation
from users.utils import generate_token, pydantic_validation
from django.contrib.auth.models import User



class RegistrationAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        data = request.data

        is_valid, msg = pydantic_validation(RegistrationValidation, data)
        if not is_valid:
            return Response(msg, status=400)
        
        user = User(**data)
        user.save()
        token = generate_token(user)
        return Response({'token':token}, status=201)