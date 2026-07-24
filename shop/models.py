from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class CropDetail(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='crop_images/')
    description = models.TextField()
    best_season = models.CharField(max_length=100)
    common_pests_diseases = models.TextField()
    recommended_fertilizer = models.TextField()

    def __str__(self):
        return self.name
    

class contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50,default="")
    phone=models.CharField(max_length=50,default="")
    desc=models.CharField(max_length=500,default="")
    
    def __str__(self):
        return self.name

    
class crop_recommend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recommend_id=models.AutoField(primary_key=True)
    nitrogen = models.FloatField(default=0.0)
    phosphorus = models.FloatField(default=0.0)
    potassium = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    ph = models.FloatField(default=0.0)
    rainfall = models.FloatField(default=0.0)
    predicted_crop = models.CharField(max_length=50 ,default='')
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.predicted_crop)