from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now








DELIVERY_STATUS_CHOICES=(
    ('pending','PENDING'),
    ('failed','FAILED'),
    ('completed','COMPLETED')
)

# Create your models here.
class Meal(models.Model):
    #name of the meal 
    name=models.CharField("Name of Meals",max_length=100)

    #description for our meal
    #optional field

    description =models.TextField("description for our meal",blank=True,null=True)
    #store the price of the meal

    price=models.DecimalField("Price($)",max_digits=10,decimal_places=2)
    image= models.ImageField(upload_to='meal_images',default='meal_images/default_meal.jpg')
    # available store the boolean true and false 
    available=models.BooleanField("Online Availability",default=False)
    #stock count:
    stock= models.IntegerField("stock count",default=0)
    def __str__(self):
        return f'{self.description}'
    
class OrderTransaction(models.Model):
    meal= models.ForeignKey(Meal,on_delete=models.CASCADE)

    customer= models.ForeignKey(User,on_delete=models.CASCADE)

    amount= models.DecimalField('Amount paid($)',max_digits=64,decimal_places=2,default=0)

    status= models.CharField('Delivery Status', max_length=9,choices=DELIVERY_STATUS_CHOICES,default='pending')

    created_at= models.DateTimeField('Date created',default=now)
    
