from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem,Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
#this import handle "not found error"
from django.shortcuts import get_object_or_404
from rest_framework import status
#Using TemplateHtmlRenderer for API output
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import renderer_classes

#for pagination
from django.core.paginator import Paginator, EmptyPage

#for users authentications(using token-based validations)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


#a view for getting all the records and displaying them as json
@api_view(['POST', 'GET'])
def menu_items(request):
  if request.method == 'GET':
    #To avoid duplication of data, we can this to 
    items = MenuItem.objects.select_related('category').all()
    #To filter through our output:
    category_name = request.query_params.get('category')
    to_price = request.query_params.get('to_price')
    perpage = request.query_params.get('perpage',default=2)
    page = request.query_params.get('page', default=1)
    
    #implementing search
    search = request.query_params.get('search')
    #ordering
    ordering = request.query_params.get('ordering')
    if category_name:
      items = items.filter(category__title = category_name)#the double underscore is for lookup.
    if to_price:
      items = items.filter(price__lte = to_price)#lte means lesser than or equal to
      
    #impleting the criteria for a search
    if search:
      items = items.filter(title__icontains = search)  
      
    #for ordering
    if ordering:
      ordering_fields = ordering.split(",")
      items = items.order_by(*ordering_fields)
    
    # items = MenuItem.objects.all()
    #from adding our serialiser instance to implement hiding the data fields
    #serialized_items = MenuItemSerializer(items, many=True, context={'request':request})# the 'many=True' is necessary when converting a list to JSON
    
    #-------------Pagination---------------------------
    paginator = Paginator(items,per_page=perpage)
    try:
      items = paginator.page(number=page)
    except EmptyPage:
      items = []
    serialized_items = MenuItemSerializer(items, many=True)
    return Response(serialized_items.data)
  
  elif request.method =='POST':
    serialized_items = MenuItemSerializer(data = request.data)
    serialized_items.is_valid(raise_exception=True)
    serialized_items.save()
    return Response(serialized_items.data,status.HTTP_201_CREATED)
  

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
  return Response({'Message':'Some secret messages, only token-authenticated users can see this'})


#Adding user roles
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
  if request.user.groups.filter(name="Manager").exists():
    return Response({'Message':'Only managers can see this'})
  else:
    return Response({"Message": "You are not allowed to read this"} ,403)
  