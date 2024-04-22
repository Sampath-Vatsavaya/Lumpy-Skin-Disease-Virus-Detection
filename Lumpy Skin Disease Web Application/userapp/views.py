from django.shortcuts import render , redirect
from userapp.models import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import urllib.request
import urllib.parse
import random
import string
from django.utils.datastructures import MultiValueDictKeyError
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
import numpy as np
from django.core.files.storage import default_storage



# model = load_model('model_inception')
model=load_model(r"D:\SOURCE CODE\WEB APPLICATION\\Lumpy Disease Full Stack\\Lumpy Disease Full Stack\\Lumphy_model.h5")


# Create your views here.

def user_index(request):
    return render(request,'user/index.html')

def user_about(request):
    return render(request,'user/about.html')

def user_contact(request):
    return render(request,'user/contact.html')


def user_services(request):
    return render(request,'user/service.html')

def user_lumpydetect(request):
      return render(request,'user/lumpydetect.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password,'jjjjjjjjjjjjjjjjjj')
        try : 
            user_data = UserModels.objects.get(email = email)
            print(user_data)
             
            if user_data.password ==  password:
                if user_data.user_status == 'accepted':
                    if user_data.Otp_Status == 'verified':
                       messages.success(request,'login successfull')
                       request.session['user_id'] = user_data.user_id
                       print('login sucessfull')
                       return redirect('user_dashboard')
                    else:
                        return redirect('otp')
                elif user_data.password == password and user_data.user_status == 'rejected':
                    messages.warning(request,"your account is rejected")
                else:
                    messages.info(request,"your account is in pending")
            else:
                messages.error(request, 'Error in Email or Password')
        except:
            print('exce[t]')
            return redirect('user_login')
    return render(request,'user/userlogin.html')

def admin_login(request):
    admin_name = 'admin@gmail.com'
    admin_pwd = 'admin'
    if request.method == 'POST':
        a_name = request.POST.get('email')
        a_pwd = request.POST.get('password')
        print(a_name, a_pwd, 'admin entered details')

        if admin_name == a_name and admin_pwd == a_pwd:
            messages.success(request, 'login successful')
            return redirect('admin_index')
        else:
            messages.error(request, 'Wrong Email Or Password')
            return redirect('admin_login')   
    return render(request,'user/adminlogin.html')

def sendSMS(user, otp, mobile):
    data = urllib.parse.urlencode({
        'username': 'Codebook',
        'apikey': '56dbbdc9cea86b276f6c',
        'mobile': mobile,
        'message': f'Hello {user}, your OTP for account activation is {otp}. This message is generated from https://www.codebook.in server. Thank you',
        'senderid': 'CODEBK'
    })
    data = data.encode('utf-8')
    # Disable SSL certificate verification
    # context = ssl._create_unverified_context()
    request = urllib.request.Request("https://smslogin.co/v3/api.php?")
    f = urllib.request.urlopen(request, data)
    return f.read()


def user_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('user')
        email = request.POST.get('email')
        contact = request.POST.get ('contact')
        password = request.POST.get('password')
        file = request.FILES['file']
        # file = request.FILES['file']
        print (request)
        print(name,username,email,contact,password,'data')
        otp = str(random.randint(1000, 9999)) 
        print(otp)
        try:
           print('try')
           UserModels.objects.get(email=email,) 
           messages.info(request, 'Mail already Registered')
           return redirect('user_registration') 
        except:
            print('except')
            # mail message
            mail_message = f'Registration Successfully\n Your 4 digit Pin is below\n {otp}'
            print(mail_message)
            send_mail("Student Password", mail_message, settings.EMAIL_HOST_USER,[email])
            # text nessage
            sendSMS(name, otp, contact)
            UserModels.objects.create( otp=otp,email=email ,password=password,name=name,contact=contact, file=file )        
            request.session['email'] = email
            messages.success(request, 'Register SUccessfull...!')
            return redirect('user_otp')
    return render(request,'user/register.html')


def user_otp (request):
    user_id = request.session['email']
    user_o =UserModels.objects.get(email = user_id)
    print(user_o,'user available')
    print(type(user_o.otp))
    print(user_o. otp,'created otp')
    # print(user_o. otp, 'creaetd otp')
    if request.method == 'POST':
        u_otp = request.POST.get('otp')
        u_otp = int(u_otp)
        print(u_otp, 'enter otp')
        if u_otp == user_o.otp:
            print('if')
            user_o.Otp_Status  = 'verified'
            user_o.save()
            messages.success(request, 'OTP  verified successfully')
            return redirect('user_login')
        else:
            print('else')
            messages.error(request, 'Error in OTP')
            return redirect('user_otp')
    return render(request,'user/otp.html')

def user_index(request):
    return render(request,'user/index.html')

def user_dashboard(request):
    return render(request,'user/dashboard.html')
def user_myprofile(request):
    user_id = request.session['user_id']
    example = UserModels.objects.get(user_id = user_id)
    print(example,'user_id')
    if request.method == 'POST' :
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        messages.success(request,'updated successful')

        example.name =name
        example.contact =contact
        example.email =email
        example.password =password
        
        if len(request.FILES)!=0:
            file = request.FILES['file']
            example.file = file
            example.name = name
            example.contact = contact
            example.email = email
            example.password = password
            example.save()
        else:
            example.name = name
            example.email = email
            example.password = password
            example.contact = contact
        #    example.file=file
            example.save()     
    return render(request,'user/myprofile.html',{'i':example})


# def user_myprofile(request):
#     user_id  = request.session['user_id']
#     user = UserModels.objects.get(pk= user_id)
#     if request.method == "POST":
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('contact')
#         try:
#             profile = request.FILES['file']
#             user.file = profile
#         except MultiValueDictKeyError:
#             profile = user.file
#         password = request.POST.get('password')
#         user.name = name
#         user.email = email
#         user.contact = phone
#         user.password = password
#         user.save()
#         messages.success(request , 'updated succesfully!')
#         return redirect('user_myprofile')
#     return render(request,'user/myprofile.html',{'i':user})




def user_feedback(request):
    views_id = request.session['user_id']
    user = UserModels.objects.get(user_id = views_id)
    if request.method == 'POST':
        u_feedback = request.POST.get('feedback')
        u_rating = request.POST.get('rating')
        if not user_feedback:
            return redirect('')
        sid=SentimentIntensityAnalyzer()
        score=sid.polarity_scores(u_feedback)
        sentiment=None
        if score['compound']>0 and score['compound']<=0.5:
            sentiment='positive'
        elif score['compound']>=0.5:
            sentiment='very positive'
        elif score['compound']<-0.5:
            sentiment='very negative'
        elif score['compound']<0 and score['compound']>=-0.5:
            sentiment='negative'
        else :
            sentiment='neutral'
        print(sentiment)
        user.star_feedback=u_feedback
        user.star_rating = u_rating
        user.save()
        UserFeedbackModels.objects.create(user_details = user, star_feedback = u_feedback, star_rating = u_rating, sentment= sentiment)
        messages.success(request,'Thankyou For Your Feedback')
    rev=UserFeedbackModels.objects.filter()    
    return render(request,'user/feedback.html')

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.models import load_model
import numpy as np

# def predict_fruit_quality_and_type(image_path):
#     # Load the fruit quality model
#     fruit_quality_model = load_model('model_inception.h5')
    
#     # Load the fruit type classification model
#     fruit_type_model = load_model('model_classifyv3.h5')
    
#     # Define labels for fruit quality and fruit type
#     fruit_quality_labels = {
#         0: 'Bad Quality ❌',
#         1: 'Good✅'
#     }
    
#     fruit_type_labels = {
#         0: 'Apple',
#         1: 'Banana',
#         2: 'Guava',
#         3: 'Lime',
#         4: 'Orange',
#         5: 'Pomegranate'
#     }
    
#     # Load and preprocess the image for both models
#     img = image.load_img(image_path, target_size=(224, 224))
#     img_array = image.img_to_array(img)
#     img_array = np.expand_dims(img_array, axis=0)
#     img_array = preprocess_input(img_array)
    
#     # Predict fruit quality
#     fruit_quality_pred = np.argmax(fruit_quality_model.predict(img_array), axis=1)
    
#     # Predict fruit type
#     fruit_type_pred = np.argmax(fruit_type_model.predict(img_array), axis=1)
    
#     # Get the corresponding labels
#     fruit_quality_result = fruit_quality_labels[fruit_quality_pred[0]]
#     fruit_type_result = fruit_type_labels[fruit_type_pred[0]]
    
#     # Format the output with a line break
#     output = f"Fruit quality:{fruit_quality_result.lower()}\nName : {fruit_type_result.lower()}."

#     return output


# image_path = r"dataset\test\good\guava_good\3.JPG"
# results = predict_fruit_quality_and_type(image_path)
# print(results)




import cv2
import matplotlib.pyplot as plt

model = load_model(r"Lumphy_model.h5")
class_labels = ['Lumpy Disease Detected ✅', 'Lumpy Disease Not Detected ❌']

def user_quality(request):
    result = "No image uploaded"
    uploaded_image_url = None  # Initialize the image URL

    if request.method == "POST" and 'image' in request.FILES:
        uploaded_image = request.FILES['image']
        file_path = default_storage.save(uploaded_image.name, uploaded_image)
        path = settings.MEDIA_ROOT + '/' + file_path
        uploaded_image_url = default_storage.url(file_path)  # Get the URL of the uploaded image
        print(path)

        # Load an image from file
        image_frame = cv2.imread(path)

        # Create subplots to display original, color, and grayscale images
        fig, axes = plt.subplots(1, 3, figsize=(15,5))

        # Display the original image
        axes[0].imshow(cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB))
        axes[0].axis('off')
        axes[0].set_title("Original Image")

        # Make predictions in color and display in subplot
        predict_and_display(image_frame, model, class_labels, display_mode='color', ax=axes[1])

        # Make predictions in grayscale and display in subplot
        predict_and_display(image_frame, model, class_labels, display_mode='grayscale', ax=axes[2])

        plt.show()

        result = prediction(path)
        print(result)
        messages.success(request, 'Lumpy Disease result Detected Successfully..')

    return render(request, 'user/lumpydetect.html', {'result': result, 'uploaded_image_url': uploaded_image_url})
def predict_and_display(frame, model, class_labels, display_mode='color', ax=None):
    img = cv2.resize(frame, (224, 224))
    img_array = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction)
    predicted_class_label = class_labels[predicted_class_index]

    if display_mode == 'color':
        display_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        title = f"Predicted Class: {predicted_class_label}"
    elif display_mode == 'grayscale':
        display_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        title = f"Gray Scale: {predicted_class_label}"
    else:
        raise ValueError("Invalid display_mode. Use 'color' or 'grayscale'.")

    if ax is not None:
        ax.imshow(display_img, cmap='gray' if display_mode == 'grayscale' else None)
        ax.axis('off')
        ax.set_title(title)
    else:
        plt.imshow(display_img, cmap='gray' if display_mode == 'grayscale' else None)
        plt.axis('off')
        plt.title(title)
        plt.show()

# Example usage:
# predict_and_display(frame, model, class_labels, display_mode='grayscale')  # Adjust parameters as needed



def prediction(path):
    img = image.load_img(path, target_size=(224, 224))
    i = image.img_to_array(img)
    i = np.expand_dims(i, axis=0)
    img = preprocess_input(i)
    pred = np.argmax(model.predict(img), axis=1)
    return class_labels[pred[0]]



# models=load_model('model_classifyv3.h5')
# ref={
#     0:'apple',
#     1:'banana',
#     2:'guava',
#     3:'lime',
#     4:'orange',
#     5:'pomegranate',

# }
# def predictionss(path):
#     img = image.load_img(path, target_size=(224, 224))
#     i = image.img_to_array(img)
#     i = np.expand_dims(i, axis=0)
#     img = preprocess_input(i)
#     pred = np.argmax(models.predict(img), axis=1)
#     return ref[pred[0]]
#     # path =
#     # prediction(path)

# def name(request):
#     result = "No image uploaded"  
#     uploaded_image_url = None  # Initialize the image URL

#     if request.method == "POST" and 'image' in request.FILES:
#         uploaded_image = request.FILES['image']
#         file_path = default_storage.save(uploaded_image.name, uploaded_image)
#         path = settings.MEDIA_ROOT + '/' + file_path
#         uploaded_image_url = default_storage.url(file_path)  # Get the URL of the uploaded image
#         print(path)
#         result = predictionss(path)
#         print(result)
#         messages.info(request, 'Fruit Name showed Successfully..')
#     return render(request, 'user/name.html', {'result': result, 'uploaded_image_url': uploaded_image_url})