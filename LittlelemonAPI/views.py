from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem,Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
#this import handle "not found error"
from django.shortcuts import get_object_or_404
from rest_framework import status

#for users authentications(using token-based validations)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes,throttle_classes

#throttlign
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle
#implementing throttle for dfferent endpoints
from .throttles import TenCallsPerMinute
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
  return Response({'Message':'Some secret messages'})


#Adding user roles
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
  if request.user.groups.filter(name="Manager").exists():
    return Response({'Message':'Only managers can see this'})
  else:
    return Response({"Message": "You are not allowed to read this"} ,403)
  
#views to implementing throttling(a way of preventing excessive calls to your api) for Anonymous users
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
  return Response({'message': 'Successful'})

#views for authenticated users
@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
  return Response({'message':"Message for the logged in users only"})