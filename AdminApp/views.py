from django.shortcuts import render, redirect
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
from sklearn.svm import SVC
import numpy as np
import sqlite3
import os
import traceback

# ===================== HELPER FUNCTIONS =====================
def load_and_preprocess_data():
    """Load and preprocess data from CSV"""
    filename = "Dataset/Crop_recommendation.csv"
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Dataset file not found: {filename}")
    
    # Load data
    data = pd.read_csv(filename, encoding='unicode_escape')
    
    # Remove rows with NaN
    data.dropna(inplace=True)
    
    # Map crop labels
    label_mapping = {
        'rice': 0, 'maize': 1, 'chickpea': 2, 'kidneybeans': 3, 'pigeonpeas': 4,
        'mothbeans': 5, 'mungbean': 6, 'blackgram': 7, 'lentil': 8, 'pomegranate': 9,
        'banana': 10, 'mango': 11, 'grapes': 12, 'watermelon': 13, 'muskmelon': 14, 'apple': 15,
        'orange': 16, 'papaya': 17, 'coconut': 18, 'cotton': 19, 'jute': 20, 'coffee': 21
    }
    
    data['label'] = data['label'].map(label_mapping)
    
    # Handle any remaining NaN in labels (unmapped values)
    data.dropna(inplace=True)
    
    # Split features and target
    X = data.iloc[:, 0:7].astype(float)
    y = data.iloc[:, 7].astype(int)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    
    return X_train, X_test, y_train, y_test


# Create your views here.
def index(request):
    return render(request, 'index.html')


def login(request):
    if 'admin' in request.session:
        return redirect('/home')
    return render(request, 'AdminApp/Login.html')


def logaction(request):
    uname = request.POST.get('username', '')
    psd = request.POST.get('password', '')

    if uname == 'Admin' and psd == 'Admin':
        request.session['admin'] = 'Admin'
        return redirect('/home')
    else:
        context = {'error': 'Invalid Username or Password'}
        return render(request, 'AdminApp/Login.html', context)


# ===================== ADMIN DASHBOARD =====================
def adminhome(request):
    if 'admin' not in request.session:
        return redirect('/login')

    con = sqlite3.connect("cropDB.db")
    cur = con.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]
    except:
        user_count = 0
    con.close()

    # Get accuracies from session or default
    decacc = request.session.get('decacc', 'Not Trained')
    svmacc = request.session.get('svmacc', 'Not Trained')
    
    # Prepare comparison data
    comparison_data = None
    if decacc != 'Not Trained' and svmacc != 'Not Trained':
        models = ['Decision Tree', 'SVM']
        accuracies = [float(decacc), float(svmacc)]
        comparison_data = {
            'models': models,
            'accuracies': accuracies,
            'best_model': models[0] if decacc > svmacc else models[1],
            'best_accuracy': max(decacc, svmacc)
        }
    else:
        comparison_data = {'error': 'Please train both models first!'}
    
    context = {
        'user_count': user_count,
        'decacc': decacc,
        'svmacc': svmacc,
        'comparison_data': comparison_data,
        'active': 'home'
    }
    return render(request, 'AdminApp/AdminHome.html', context)


# ===================== USER MANAGEMENT =====================
def user_management(request):
    if 'admin' not in request.session:
        return redirect('/login')

    con = sqlite3.connect("cropDB.db")
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
    except:
        users = []
    con.close()

    context = {'users': users, 'active': 'users'}
    return render(request, 'AdminApp/UserManagement.html', context)


def delete_user(request, user_id):
    if 'admin' not in request.session:
        return redirect('/login')

    con = sqlite3.connect("cropDB.db")
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (user_id,))
    con.commit()
    con.close()

    return redirect('/user_management')


def view_user_details(request, user_id):
    if 'admin' not in request.session:
        return redirect('/login')

    con = sqlite3.connect("cropDB.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
    con.close()

    if user:
        context = {'user': user, 'active': 'users'}
        return render(request, 'AdminApp/UserDetails.html', context)
    return redirect('/user_management')


# ===================== DATA MANAGEMENT =====================
def data_management(request):
    if 'admin' not in request.session:
        return redirect('/login')

    filename = "Dataset/Crop_recommendation.csv"
    try:
        if not os.path.exists(filename):
            context = {'error': 'Dataset file not found. Please upload a CSV file.', 'active': 'data'}
        else:
            data = pd.read_csv(filename, encoding='unicode_escape')

            # Check if user wants to view full data or summary
            view_mode = request.GET.get('view', 'summary')  # 'summary' or 'full'

            if view_mode == 'full':
                # Show all data
                data_preview = data.to_html(classes='table table-bordered table-striped', index=False)
                sample_rows = len(data)
                show_full_data = True
            else:
                # Show sample of 7 rows instead of all data
                data_preview = data.head(7).to_html(classes='table table-bordered table-striped', index=False)
                sample_rows = 7
                show_full_data = False

            # Data quality info
            data_quality = {
                'total_rows': len(data),
                'total_columns': len(data.columns),
                'missing_values': int(data.isnull().sum().sum()),
                'duplicate_rows': int(data.duplicated().sum()),
                'numeric_features': len(data.select_dtypes(include=[np.number]).columns),
                'categorical_features': len(data.select_dtypes(include=['object']).columns)
            }

            context = {
                'rows': len(data),
                'columns': len(data.columns),
                'data_preview': data_preview,
                'column_names': list(data.columns),
                'data_quality': data_quality,
                'sample_rows': sample_rows,
                'show_full_data': show_full_data,
                'view_mode': view_mode,
                'active': 'data'
            }
    except Exception as e:
        context = {'error': f'Could not load data: {str(e)}', 'active': 'data'}

    return render(request, 'AdminApp/DataManagement.html', context)


# ===================== DATA PREPROCESSING =====================
def preprocess(request):
    if 'admin' not in request.session:
        return redirect('/login')

    try:
        X_train, X_test, y_train, y_test = load_and_preprocess_data()
        
        # Store count info only, not the actual data
        request.session['preprocessed'] = True
        request.session['train_count'] = len(X_train)
        request.session['test_count'] = len(X_test)
        request.session.modified = True
        
        context = {
            'data': str(len(X_train) + len(X_test)), 
            'train': str(len(X_train)), 
            'test': str(len(X_test)), 
            'active': 'preprocess'
        }
    except Exception as e:
        print(f"Preprocess Error: {str(e)}")
        traceback.print_exc()
        context = {
            'error': f'Preprocessing failed: {str(e)}',
            'active': 'preprocess'
        }
        
    return render(request, 'AdminApp/Preprocess.html', context)


# ===================== MODEL TRAINING - DECISION TREE =====================
def decision(request):
    if 'admin' not in request.session:
        return redirect('/login')

    try:
        # Load data fresh from CSV
        X_train, X_test, y_train, y_test = load_and_preprocess_data()
        
        # Train model
        print("Training Decision Tree Model...")
        decmodel = DecisionTreeClassifier(random_state=0, max_depth=10)
        decmodel.fit(X_train, y_train)
        
        # Ensure model directory exists
        os.makedirs("model", exist_ok=True)
        
        # Save model
        joblib.dump(decmodel, "model/DecModel.joblib")
        print("Decision Tree model saved successfully")
        
        # Calculate accuracy
        pred = decmodel.predict(X_test)
        acc = accuracy_score(y_test, pred)
        decacc = round(acc * 100, 2)
        
        # Store in session
        request.session['decacc'] = decacc
        request.session.modified = True
        
        print(f"Decision Tree Accuracy: {decacc}%")
        
        context = {
            'data': f'✅ Decision Tree Model Trained Successfully! Accuracy: {decacc}%', 
            'acc': str(decacc), 
            'active': 'decision'
        }
    except Exception as e:
        error_msg = str(e)
        print(f"Decision Tree Training Error: {error_msg}")
        traceback.print_exc()
        context = {
            'data': '❌ Decision Tree training failed', 
            'acc': '0', 
            'error': error_msg, 
            'active': 'decision'
        }

    return render(request, 'AdminApp/DecAlgorithms.html', context)


# ===================== MODEL TRAINING - SVM =====================
def svm(request):
    if 'admin' not in request.session:
        return redirect('/login')

    try:
        # Load data fresh from CSV
        X_train, X_test, y_train, y_test = load_and_preprocess_data()
        
        # Train model
        print("Training SVM Model...")
        svmmodel = SVC(kernel='rbf', random_state=0, gamma='scale')
        svmmodel.fit(X_train, y_train)
        
        # Ensure model directory exists
        os.makedirs("model", exist_ok=True)
        
        # Save model
        joblib.dump(svmmodel, "model/svmacc.joblib")
        print("SVM model saved successfully")
        
        # Calculate accuracy
        pred = svmmodel.predict(X_test)
        acc = accuracy_score(y_test, pred)
        svmacc = round(acc * 100, 2)
        
        # Store in session
        request.session['svmacc'] = svmacc
        request.session.modified = True
        
        print(f"SVM Accuracy: {svmacc}%")
        
        context = {
            'data': f'✅ SVM Model Trained Successfully! Accuracy: {svmacc}%', 
            'acc': str(svmacc), 
            'active': 'svm'
        }
    except Exception as e:
        error_msg = str(e)
        print(f"SVM Training Error: {error_msg}")
        traceback.print_exc()
        context = {
            'data': '❌ SVM training failed', 
            'acc': '0', 
            'error': error_msg, 
            'active': 'svm'
        }

    return render(request, 'AdminApp/SVMAlgorithms.html', context)


# ===================== MODEL COMPARISON =====================
def comparison(request):
    if 'admin' not in request.session:
        return redirect('/login')

    decacc = request.session.get('decacc', 0)
    svmacc = request.session.get('svmacc', 0)
    
    if decacc == 0 or svmacc == 0:
        context = {
            'error': '⚠️ Please train both models first! Go to "Train DT" and "Train SVM"', 
            'active': 'comparison'
        }
    else:
        models = ['Decision Tree', 'SVM']
        accuracies = [float(decacc), float(svmacc)]
        context = {
            'models': models,
            'accuracies': accuracies,
            'best_model': models[0] if decacc > svmacc else models[1],
            'best_accuracy': max(decacc, svmacc),
            'active': 'comparison'
        }

    return render(request, 'AdminApp/ModelComparison.html', context)


# ===================== MODEL MANAGEMENT =====================
def model_management(request):
    if 'admin' not in request.session:
        return redirect('/login')

    decacc = request.session.get('decacc', 0)
    svmacc = request.session.get('svmacc', 0)
    
    context = {
        'dec_accuracy': round(decacc, 2) if decacc > 0 else 'Not Trained',
        'svm_accuracy': round(svmacc, 2) if svmacc > 0 else 'Not Trained',
        'active': 'model'
    }
    return render(request, 'AdminApp/ModelManagement.html', context)


# ===================== LOGOUT =====================
def admin_logout(request):
    if 'admin' in request.session:
        del request.session['admin']
    return redirect('/login')


# ===================== UPLOAD DATASET =====================
def upload(request):
    if 'admin' not in request.session:
        return redirect('/login')

    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        if uploaded_file.name.endswith('.csv'):
            os.makedirs("Dataset", exist_ok=True)
            with open('Dataset/Crop_recommendation.csv', 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            context = {'message': '✅ Dataset uploaded successfully!', 'active': 'upload'}
        else:
            context = {'error': '❌ Please upload a CSV file.', 'active': 'upload'}
    else:
        context = {'active': 'upload'}

    return render(request, 'AdminApp/Upload.html', context)
