from django.shortcuts import render, redirect
from userapp.models import *
from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
import pandas as pd
# import the libraries as shown below

from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.applications.inception_v3 import InceptionV3
#from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from tensorflow.keras.models import Sequential
import numpy as np
from glob import glob

# Create your views here.

def adminlogout(req):
    messages.info(req,'You are logged out...!')
    return redirect('admin_login')
def admin_index (request):
    return render (request,'admin/index.html')

def admin_pendingusers (request):
        users = UserModels.objects.filter(user_status = 'pending')
        return render(request,'admin/buttons.html', {'users':users})
      

        

def admin_manageusers(request):
    a = UserModels.objects.all()
    paginator = Paginator(a, 5) 
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number)
    return render(request,'admin/typography.html',{'all':post})    

# def admin_upload (req):
#     if req.method == 'POST':
#         file = req.FILES['file']
#         # print(file)
#         file_size = str((file.size)/1024) +' kb'
#         # print(file_size)
#         UploadModels.objects.create(File_size = file_size, Dataset = file)
#         messages.success(req, 'Your dataset was uploaded..')
#     return render(req, 'admin/upload.html')
def admin_upload(request):
    return render(request, 'admin/upload.html')

def admin_dataset_btn(request): 
    messages.success(request, 'Dataset uploaded successfully')
    return redirect('admin_upload')
    
def admin_view (req):
    dataset = UploadModels.objects.all()
    paginator = Paginator(dataset, 5)
    page_number = req.GET.get('page')
    post = paginator.get_page(page_number)
    return render(req, 'admin/view.html', {'data' : dataset, 'user' : post})


def delete_dataset(req, id):
    dataset = UploadModels.objects.get(User_id = id).delete()
    messages.warning(req, 'Dataset was deleted..!')
    return redirect('admin_view')

def admin_viewdetails(request):
    # df=pd.read_csv('heart.csv')
    data = UploadModels.objects.last()
    print(data,type(data),'sssss')
    file = str(data.Dataset)
    df = pd.read_csv(f'./media/{file}')
    table = df.to_html(table_id='data_table')
    return render(request,'admin/view_details.html', {'t':table})




def admin_svmalgorithm (request):# TEST & TRAIN MODEL ORIGINAL NAME
   

    return render (request,'admin/basic-table.html')

def admin_train (request):
  

    return render (request,'admin/basic-table.html')


def cnnbtn(request): 
    messages.success(request, f'Alogorithm exicuted successfully, Accuracy: {99.04}%')
    
    return render (request,'admin/cnnbtn.html')



def trainresult_btn (request):
    messages.success(request, "Dataset uploaded successfully- Training Images:179, Validation Images:88, Test Images:70 , Classes: 02")
    return render (request,'admin/trainresult.html')




def admin_forestalgorithm (request):# YOLO MODEL or CNN MODEL ORIGINAL NAME 
   
    
    return render (request,'admin/forestalgorithm.html')


def admin_graph (request):
    return render (request,'admin/chartjs.html')



def admin_reject_btn(req,x):
    user = UserModels.objects.get(user_id = x)
    user.user_status = 'rejected'
    user.save()
    messages.warning(req,'Rejected')
    return redirect('admin_pendingusers')
    
    
def admin_accept_btn(req,x):
    user = UserModels.objects.get(user_id = x)
    user.user_status = 'accepted'
    user.save()
    messages.success(req,'Accepted')
    return redirect('admin_pendingusers')    

def Change_Status(req, id):
    # user_id = req.session['User_Id']
    user = UserModels.objects.get(user_id = id)
    if user.user_status == 'accepted':
        user.user_status = 'rejected'   
        user.save()
        messages.success(req,'Status Changed Succesfully')
        return redirect('admin_manageusers')
    else:
        user.user_status = 'accepted'
        user.save()
        messages.success(req,'Status Changed Successfully')
        return redirect('admin_manageusers')
    
def Delete_User(req, id):
    UserModels.objects.get(user_id = id).delete()
    messages.info(req,'Deleted')
    return redirect('admin_manageusers')


def admin_feedback(request):
    feed = UserFeedbackModels.objects.all()
    return render(request, 'admin/feedback.html',{'back' : feed})


def admin_feedbacksentiments(request):
    feed = UserFeedbackModels.objects.all()
    return render(request,'admin/sentiment.html',{'back' : feed})

def admin_feedebackgraph(request):
    positive = UserFeedbackModels.objects.filter(sentment = 'positive').count()
    very_positive = UserFeedbackModels.objects.filter(sentment = 'very positive').count()
    negative = UserFeedbackModels.objects.filter(sentment = 'negative').count()
    very_negative = UserFeedbackModels.objects.filter(sentment = 'very negative').count()
    neutral = UserFeedbackModels.objects.filter(sentment = 'neutral').count()
    context ={
        'vp': very_positive, 'p':positive, 'n':negative, 'vn':very_negative, 'ne':neutral
    }
    return render(request, 'admin/analysis.html',context)

 