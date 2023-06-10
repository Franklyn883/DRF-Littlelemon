
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
#this import handle "not found error"
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
  return Response({'message':'Some secret message'})