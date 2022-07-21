from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *

class PersonView(APIView):

    def post(self, request, format=None):
        serializer = Person_Serializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
