from django.db import models
from pkg_resources import require


class AH_Dump(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name  
    
class AH_Item(models.Model):
    ah = models.ForeignKey(AH_Dump, on_delete=models.CASCADE)
    a_id = models.CharField(max_length=50, unique=True)
    item_id = models.CharField(max_length=50)
    item = models.CharField(max_length=500)
    bid = models.CharField(max_length=50)
    buyout = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    time_left = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return self.item_id  
    
class Item(models.Model):  
    item_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    item_url = models.CharField(max_length=500, default="")
    item_data = models.CharField(max_length=5000, default="")
    item_media = models.CharField(max_length=5000, default="")
    def __str__(self):
        return self.name
    
