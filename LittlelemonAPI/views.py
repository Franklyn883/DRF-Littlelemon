from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
class MenuItemsView(generics.ListCreateAPIView):
  queryset = MenuItem.objects.all()
  serializer_class = MenuItemSerializer
  
  
# To create a single item view
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
  queryset = MenuItem.objects.all()
  serializer_class = MenuItemSerializer
  
  
#creating a view function that shows the menu items, here on my serialization lessons
def 