
from django.shortcuts import render
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from .models import *
from .models import PatientDetails
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.contrib import messages



def patient(request):
    if request.method == "POST":
        data = request.POST
        new_patient = {
            'HAEMATOCRIT': [float(data.get('texthaematocrit'))],
            'HAEMOGLOBINS': [float(data.get('texthaemoglobins'))],
            'ERYTHROCYTE': [float(data.get('texterythrocyte'))],
            'LEUCOCYTE': [float(data.get('textleucocyte'))],
            'THROMBOCYTE': [float(data.get('textthrombocyte'))],
            'MCH': [float(data.get('textmch'))],
            'MCHC': [float(data.get('textmchc'))],
            'MCV': [float(data.get('textmcv'))],
            'AGE': [int(data.get('textage'))],
            'SEX': [0 if data.get('textsex') == 'F' else 1],
        }
        new_patient_df = pd.DataFrame.from_dict(new_patient)

        if 'buttonpredict' in request.POST:
            path = "C:\\Users\\akash\\Desktop\\PROJECT\\2024_projects\\37_PatientTreatmentClassification\\data.csv"
            dataset = pd.read_csv(path)
            dataset['SEX'] = dataset['SEX'].map({'F': 0, 'M': 1})
            inputs = dataset.drop(['SOURCE'], axis=1)
            output = dataset['SOURCE']
            
            x_train, x_test, y_train, y_test = train_test_split(inputs, output, train_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=200, random_state=42)
            model.fit(x_train, y_train.values.ravel())
            
            prediction = model.predict(new_patient_df)
            
            # Add the if statement to display a user-friendly messagein care patient, out = out care patient, out = out care patient
            result_message = "In Care" if prediction[0] == 'in' else "Out Care"
            return render(request, 'patient.html', context={'result': "Prediction: " + result_message})
    return render(request, 'patient.html')


def index(request):
  return render(request,'index.html')

def home(request):
    return render(request,'home.html')

def about (request):
    return render(request,'about.html')

def registration(request):
    if request.method == 'POST':
        firstname = request.POST['textfirstname']
        lastname = request.POST['textlastname']
        username = request.POST['textusername']
        password = make_password(request.POST['textpassword'])  # hash the password

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return render(request, 'registration.html')
        else:
            user = User(first_name=firstname, last_name=lastname, username=username, password=password)
            user.save()
            messages.success(request, 'Registration successful')
            return render(request, 'registration.html')
    else:
        return render(request, 'registration.html')

# def patientdetails(request):
#   if(request.method=="POST"):
#     data=request.POST
#     patname=data.get('textpatname')
#     patemail=data.get('textpatemail')
#     PatientDetails.objects.create(PAT_NAME=patname,PAT_EMAIL=patemail)
#     result="Patient details saved successfully";
#     return render(request,'patientdetails.html',context={'result': result})
#   return render(request,'patientdetails.html')

# def patientdetailsview(request):
#     result= PatientDetails.objects.all()
#     return render(request,'patientdetailsview.html',context={'result': result})

# def patientdetailsdelete(request,id):
#     result= PatientDetails.objects.get(id=id)
#     result.delete()
#     return redirect('/patientdetailsview/')

# def patientdetailsupdate(request,id):
#     result= PatientDetails.objects.get(id=id)
#     if(request.method=="POST"):
#        data=request.POST
#        patname=data.get('textpatname')
#        patemail=data.get('textpatemail')
#        result.PAT_NAME=patname
#        result.PAT_EMAIL=patemail
#        result.save()
#        return redirect('/patientdetailsview/')
#     return render(request,'patientdetailsupdate.html',context={'result':result})

def userlogin(request):
  if request.method=="POST":
    data=request.POST
    username=data.get('textusername')
    password=data.get('textpassword')
    user= User.objects.filter(username=username)
    if not user.exists():
       result="Invalid username"
       return render(request,'login.html',context={'result':result})
    user= authenticate(username=username,password=password)
    if(user is None):
       result="Invalid Password"
       return render(request,'login.html',context={'result':result})
    else:
       login(request,user)
       return redirect('/index/')
  return render(request,'login.html')




def userlogout(request):
   logout(request)
   return redirect('/userlogin')