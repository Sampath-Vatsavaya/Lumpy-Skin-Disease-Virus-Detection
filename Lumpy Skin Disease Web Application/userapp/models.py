from django.db import models
import datetime
# Create your models here.
class UserModels(models.Model):
    user_id = models.AutoField(primary_key=True)
    date = models.DateField(default=datetime.date.today)
    name = models.TextField(max_length=50, null=True)
    # username = models.TextField(max_length=25, null=True)
    contact = models.TextField(max_length=25, null=True)
    email = models.EmailField(max_length=200, null=True)
    password = models.TextField( max_length=8, null=True)   
    file = models.FileField( upload_to='images', null=True)
    user_status=models.TextField(max_length=30,default='pending',null=True)
    Otp_Status = models.TextField(max_length=20, default='pending')
    otp = models.IntegerField(null=True)
    
    class  Meta:
        db_table = 'user_details'



class UserFeedbackModels(models.Model):
    feed_id = models.AutoField(primary_key=True)
    star_feedback = models.TextField(max_length=900)
    star_rating = models.CharField(max_length=100,null=True)
    star_Date = models.DateTimeField(auto_now_add=True, null=True)
    user_details = models.ForeignKey(UserModels, on_delete=models.CASCADE)
    sentment = models.TextField(max_length=20,null=True)
    class Meta:
        db_table = 'feedback_Details'        


class UploadModels(models.Model):
    User_id = models.AutoField(primary_key = True)
    Dataset = models.FileField(upload_to='', null=True)
    File_size = models.CharField(max_length = 100) 
    Date_Time = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'upload_dataset'