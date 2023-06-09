from rest_framework.response import Response
from rest_framework import viewsets
from .models import MenuItem
from .serializers import MenuItemSerializer

#declare our class view and extend the modelviewset class
class MenuItemsViewSet(viewsets.ModelViewSet):
  queryset = MenuItem.objects.all()
  serializer_class = MenuItemSerializer
  #here we add the ordering and sorting fields
  ordering_fields = ['price', 'inventory']
  search_fields = ['title', 'category__title']