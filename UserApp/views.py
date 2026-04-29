from django.shortcuts import render
import sqlite3
import joblib
import pandas as pd
import cv2
import imutils
import glob


# Create your views here.
def login(request):
    return render(request,'userapp/Login.html')
def register(request):
    return render(request,'userapp/Register.html')

def RegAction(request):
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    mobile = request.POST.get('mobile', '').strip()
    address = request.POST.get('address', '').strip()
    username = request.POST.get('username', '').strip()
    password = request.POST.get('password', '').strip()

    if not name or not email or not mobile or not address or not username or not password:
        context = {'data': 'Please fill in all details before registering.'}
        return render(request, 'UserApp/Register.html', context)

    try:
        con = sqlite3.connect("cropDB.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users (name, email, mobile, address, username, password) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, email, mobile, address, username, password))
        con.commit()
        success = cur.rowcount > 0
        con.close()

        if success:
            context = {'data': 'Registration Successful...!!'}
        else:
            context = {'data': 'Registration Failed...!!'}
        return render(request, 'UserApp/Register.html', context)
    except Exception as e:
        context = {'data': 'Registration Failed...!! ' + str(e)}
        return render(request, 'UserApp/Register.html', context)

def logaction(request):
    username=request.POST.get('username')
    password=request.POST.get('password')
    con = sqlite3.connect("cropDB.db")
    cur=con.cursor()
    cur.execute("select *  from users where username='"+username+"'and password='"+password+"'")
    data=cur.fetchone()
    if data is not None:
        request.session['user']=username
        request.session['userid']=data[0]
        return render(request,'UserApp/UserHome.html')
    else:
        context={'data':'Login Failed ....!!'}
        return render(request,'UserApp/Login.html',context)
def home(request):
    return render(request,'UserApp/UserHome.html')

def viewprofile(request):
    uid=str(request.session['userid'])
    con = sqlite3.connect("cropDB.db")
    cur=con.cursor()
    cur.execute("select * from users where id='"+uid+"'")
    data=cur.fetchall()
    strdata="<table border=1 style='margin:0px;'><tr><th>Name</th><th>Email</th><th>Mobile</th><th>Address</th><th>Username</th></tr>"
    for i in data:
        strdata+="<tr><td>"+str(i[1])+"</td><td>"+str(i[2])+"</td><td>"+str(i[3])+"</td><td>"+str(i[4])+"</td><td>"+str(i[5])+"</td></tr>"
    context={'data':strdata}
    return render(request,'UserApp/ViewProfile.html',context)


def uploadtest(request):
    return render(request,'UserApp/UploadTest.html')

def CropAction(request):
    try:
        # Get parameters and convert to float
        a = float(request.POST.get('nitrogen', 0))
        b = float(request.POST.get('phosphorous', 0))
        c = float(request.POST.get('potassium', 0))
        d = float(request.POST.get('temp', 0))
        e = float(request.POST.get('humidity', 0))
        f = float(request.POST.get('phvalue', 0))
        g = float(request.POST.get('rainfall', 0))

        # Load model and make prediction
        dec_model = joblib.load("model/DecModel.joblib")
        pred = dec_model.predict([[a, b, c, d, e, f, g]])
        pred_index = int(pred[0])
        print("predicted value: " + str(pred_index))
        
        # Load crop data
        dataset = pd.read_excel("Dataset/cropname.xlsx")
        
        # Validate prediction index
        if pred_index < 0 or pred_index >= len(dataset):
            raise ValueError(f"Prediction index {pred_index} out of range")
        
        crop_name = str(dataset.name[pred_index])
        planting_method = str(dataset.planting_method[pred_index])
        duration = str(dataset.Duration[pred_index])
        months = str(dataset.planting_months[pred_index])
        
        # Add image path for the crop
        image_path = f'/static/img/{crop_name.lower()}.jpg'
        
        context = {
            'data': crop_name,
            'method': planting_method,
            'duration': duration,
            'months': months,
            'image': image_path
        }
        return render(request, 'UserApp/PredictedData.html', context)
    
    except ValueError as e:
        error_msg = f'❌ Error: Invalid input values. Please enter numeric values only. ({str(e)})'
        print(error_msg)
        context = {'data': error_msg}
        return render(request, 'UserApp/UploadTest.html', context)
    except FileNotFoundError as e:
        error_msg = f'❌ Error: File not found. {str(e)}'
        print(error_msg)
        context = {'data': error_msg}
        return render(request, 'UserApp/UploadTest.html', context)
    except Exception as e:
        error_msg = f'❌ Error: {str(e)}'
        print(error_msg)
        context = {'data': error_msg}
        return render(request, 'UserApp/UploadTest.html', context)

def feedbackAction(request):
    try:
        a = request.POST.get('cname', '').strip()
        b = request.POST.get('feed', '').strip()
        uname = request.session.get('user', '')

        # Validate inputs
        if not a or not b or not uname:
            context = {'msg': '❌ Error: All fields are required. Please fill in the crop name and feedback.'}
            return render(request, 'UserApp/PredictedData.html', context)

        # Use parameterized queries to prevent SQL injection
        con = sqlite3.connect("cropDB.db")
        cur = con.cursor()

        # Insert feedback using parameterized query
        cur.execute("INSERT INTO feedback (username, cropname, feedback) VALUES (?, ?, ?)", (uname, a, b))
        con.commit()

        # Get all feedback for display
        cur.execute("SELECT * FROM feedback")
        data = cur.fetchall()

        strdata = "<table border='1' style='width:100%; border-collapse:collapse;'><tr><th>UserName</th><th>CropName</th><th>Feedback</th></tr>"
        for d in data:
            strdata += f"<tr><td>{d[1]}</td><td>{d[2]}</td><td>{d[3]}</td></tr>"
        strdata += "</table>"

        context = {'msg': '✅ Feedback Submitted Successfully!', 'data': strdata}
        con.close()
        return render(request, 'UserApp/Feedback.html', context)

    except Exception as e:
        print(f"Error in feedbackAction: {str(e)}")
        context = {'msg': f'❌ Error submitting feedback: {str(e)}'}
        return render(request, 'UserApp/PredictedData.html', context)

def feedback(request):
    con = sqlite3.connect("cropDB.db")
    cur=con.cursor()
    cur.execute("select * from feedback")
    data=cur.fetchall()
    strdata="<table><tr><th>UserName</th><th>CropName</th><th>Feedback</th></tr>"
    for d in data:
        strdata+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td></tr>"
    context={'data':strdata}
    return render(request,'UserApp/Feedback.html', context)


