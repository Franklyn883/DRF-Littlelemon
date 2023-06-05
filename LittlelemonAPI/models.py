from django.db import models

#to demonstrate how to use a relationship serializer we will be creating an addition model
class Category(models.Model):
  slug = models.SlugField()
  title = models.CharField(max_length=225)
  def __str__(self):
    return self.title
  
# Create your models here.
class MenuItem(models.Model):
  title = models.CharField(max_length=255)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  inventory = models.SmallIntegerField()
  #Relationship serializers: here we create a relationship with the category table.
  category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)
  
  def __str__(self):
    return self.title