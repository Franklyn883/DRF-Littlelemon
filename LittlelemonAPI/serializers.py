from rest_framework import serializers
from .models import MenuItem,Category
from decimal import Decimal
from rest_framework.validators import UniqueValidator,UniqueTogetherValidator
#for cleaning your date
import bleach

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
  #
  # price = serializers.DecimalField(max_digits=6,decimal_places=2, min_value=2)
  #--------------Adding Data Validation to your serializers with validate_field method----------------
  # def validate_price(self,value):
  #   if (value < 2):
  #     raise serializers.ValidationError("Price should be more that or equal to 2")
     
  # def validate_stock(self,value):
  #   if(value < 0):
  #     raise serializers.ValidationError("Stock cannot be Negative")
  
  #-----------Adding validation using Validate() method:This can be used to add validation to multiple fields
  #____________________
  def validate(self, attrs):
    attrs['title'] = bleach.clean(attrs['title'])
    if(attrs['price']<2):
      raise serializers.ValidationError("Price should be greater than or equal to 2")
    if(attrs['inventory']<0):
      raise serializers.ValidationError("Stock should not be negative")
    return super().validate(attrs)
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
  #  #validation
  #   extra_kwargs = {
  #     "price":{"min_value":2},
  #     "stock":{"source":"inventory", "min_value":0}
      
  #   }
  validators = [
    UniqueTogetherValidator(
      queryset=MenuItem.objects.all(),
      fields=['title','price']
    ),
  ]
    # adding a calculated field to our serializer
  def calculate_tax(self, product:MenuItem):
      pay_after_tax = product.price * Decimal(1.1)
      return round(pay_after_tax,3)
  
 