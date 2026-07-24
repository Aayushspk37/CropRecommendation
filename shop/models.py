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

    class Meta:
        ordering = ['name']
        verbose_name = 'Crop Detail'
        verbose_name_plural = 'Crop Details'


class contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=500, default="")
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-msg_id']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'


class crop_recommend(models.Model):
    recommend_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nitrogen = models.FloatField(default=0.0)
    phosphorus = models.FloatField(default=0.0)
    potassium = models.FloatField(default=0.0)
    temperature = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    ph = models.FloatField(default=0.0)
    rainfall = models.FloatField(default=0.0)
    predicted_crop = models.CharField(max_length=50, default='')
    timestamp = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.predicted_crop} - {self.timestamp.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Crop Recommendation'
        verbose_name_plural = 'Crop Recommendations'