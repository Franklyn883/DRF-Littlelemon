from rest_framework import serializers
from .models import MenuItem,Category
from decimal import Decimal
#We import the Category Model here inorder to be able to display the name
# from .models import Category


#date:4-o6-2023
#with the help of serializer you can hide any field you don't want to display to the public

# class MenuItemSerializer(serializers.Serializer):
#   #the fields included here will be the one displayed in the browser, we can add more fields
#   id = serializers.IntegerField()
#   title = serializers.CharField(max_length = 255)
#   price = serializers.DecimalField(max_digits=5, decimal_places=2)
#   inventory = serializers.IntegerField()
  
#Add the Category Model to our seializers---------------
class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ['id','slug','title']  
  

# A quicker and most effective way of dealing with serializer
#class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
class MenuItemSerializer(serializers.ModelSerializer):
  #we can change the name of a field using this method:
  stock = serializers.IntegerField(source='inventory')
    #to add a calculated field to our serializer NOTE: this field is not added to the DB
  price_after_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
  #inorder to be able to display the category title, With this we can be able to display the Category Method
  #creating a hyperlink----------------------
  #category = serializers.HyperlinkedRelatedField(
  #   queryset =Category.objects.all(),
  #   view_name='category-detail'
  # )
  category = CategorySerializer(read_only=True)
  # To bring even more detailed result from the Category model
 # category = CategorySerializer()
  category_id = serializers.IntegerField(write_only=True)
  class Meta: 
    model = MenuItem
    #Relationship serializers:here we add the category field to the model
    fields = ['id','title','price','stock','price_after_tax','category', 'category_id']
    #this is another way of achieving relation serializers
   # depth = 1
    
    # adding a calculated field to our serializer
  def calculate_tax(self, product:MenuItem):
      pay_after_tax = product.price * Decimal(1.1)
      return round(pay_after_tax,3)
  
 