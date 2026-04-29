#!/usr/bin/env python
"""
Retrain Decision Tree and SVM models with current scikit-learn version
This fixes the pickle compatibility issue
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
import os

print("=" * 70)
print("🔄 Retraining ML Models with Current scikit-learn Version")
print("=" * 70)

try:
    # Load dataset
    print("\n📂 Loading dataset...")
    filename = "Dataset/Crop_recommendation.csv"
    
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found!")
        exit(1)
    
    data = pd.read_csv(filename, encoding='unicode_escape')
    print(f"✓ Dataset loaded: {len(data)} records")
    
    # Data preprocessing
    print("\n🔧 Preprocessing data...")
    data.dropna(inplace=True)
    
    # Map crop labels
    label_mapping = {
        'rice': 0, 'maize': 1, 'chickpea': 2, 'kidneybeans': 3, 'pigeonpeas': 4,
        'mothbeans': 5, 'mungbean': 6, 'blackgram': 7, 'lentil': 8, 'pomegranate': 9,
        'banana': 10, 'mango': 11, 'grapes': 12, 'watermelon': 13, 'muskmelon': 14, 'apple': 15,
        'orange': 16, 'papaya': 17, 'coconut': 18, 'cotton': 19, 'jute': 20, 'coffee': 21
    }
    
    data['label'] = data['label'].map(label_mapping)
    print(f"✓ Encoded labels: {len(label_mapping)} crop types")
    
    # Split features and target
    X = data.iloc[:, 0:7]  # Features: N, P, K, temp, humidity, ph, rainfall
    y = data.iloc[:, 7]    # Target: crop label
    
    print(f"✓ Features shape: {X.shape}")
    print(f"✓ Target shape: {y.shape}")
    
    # Train-test split
    print("\n📊 Splitting data (80-20 split)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    print(f"✓ Training samples: {len(X_train)}")
    print(f"✓ Test samples: {len(X_test)}")
    
    # Train Decision Tree
    print("\n🌳 Training Decision Tree Classifier...")
    dt_model = DecisionTreeClassifier(random_state=0)
    dt_model.fit(X_train, y_train)
    dt_pred = dt_model.predict(X_test)
    dt_acc = accuracy_score(y_test, dt_pred) * 100
    print(f"✓ Decision Tree Accuracy: {dt_acc:.2f}%")
    
    # Save Decision Tree model
    model_path = "model/DecModel.joblib"
    os.makedirs("model", exist_ok=True)
    joblib.dump(dt_model, model_path)
    print(f"✓ Saved: {model_path}")
    
    # Train SVM
    print("\n🎯 Training Support Vector Machine (SVM)...")
    svm_model = SVC(kernel='rbf', random_state=0)
    svm_model.fit(X_train, y_train)
    svm_pred = svm_model.predict(X_test)
    svm_acc = accuracy_score(y_test, svm_pred) * 100
    print(f"✓ SVM Accuracy: {svm_acc:.2f}%")
    
    # Save SVM model
    svm_path = "model/svmacc.joblib"
    joblib.dump(svm_model, svm_path)
    print(f"✓ Saved: {svm_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Models retrained and saved with current scikit-learn")
    print("=" * 70)
    print(f"\n📈 Model Performance:")
    print(f"   Decision Tree Accuracy: {dt_acc:.2f}%")
    print(f"   SVM Accuracy: {svm_acc:.2f}%")
    print(f"\n✅ You can now use the 'Upload Test Data' feature!")
    print("=" * 70)
    
except Exception as e:
    print(f"\n❌ Error during training: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)
