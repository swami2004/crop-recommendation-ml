## 🌾 Crop Recommendation System - Quick Setup Guide

### Prerequisites
- Python 3.x installed on your system
- Git (optional, for cloning)

---

### ⚡ Quick Start (3 Steps)

#### **Step 1: Navigate to Project**
```bash
cd c:\Users\tamid\Downloads\CropRecommendAndSuggesion\CropRecommendAndSuggesion
```

#### **Step 2: Install Dependencies** (Choose ONE)

**Option A - Using requirements.txt (Recommended):**
```bash
python -m pip install -r requirements.txt
```

**Option B - Manual Installation:**
```bash
python -m pip install Django pandas scikit-learn joblib opencv-python imutils matplotlib numpy openpyxl
```

**Option C - Using setup script:**
```bash
python setup.py
```

#### **Step 3: Run the Server**
```bash
python manage.py runserver
```

Then open your browser: **http://localhost:8000**

---

### 📋 What Gets Installed

| Package | Purpose |
|---------|---------|
| **Django 2.2** | Web framework |
| **pandas** | Data manipulation & Excel handling |
| **scikit-learn** | Machine learning models |
| **joblib** | Model serialization |
| **opencv-python** | Image processing |
| **imutils** | OpenCV utilities |
| **matplotlib** | Data visualization |
| **numpy** | Numerical computing |
| **openpyxl** | Excel file reading |

---

### 🔐 Login Credentials

**Admin Panel:** http://localhost:8000/
- Username: `Admin`
- Password: `Admin`

**Sample User Accounts:**
| Username | Password |
|----------|----------|
| rajesh | pass123 |
| priya | priya789 |
| arjun | arjun456 |
| neha | neha321 |
| vikram | vikram654 |

---

### ✨ Key Features

1. **Admin Panel:**
   - Upload dataset
   - Preprocess data
   - Train Decision Tree model
   - Train SVM model
   - Compare model performance

2. **User Portal:**
   - Register & Login
   - Input soil parameters (N, P, K, Temp, Humidity, pH, Rainfall)
   - Get crop recommendations
   - View profile
   - Submit feedback

---

### 🐛 Troubleshooting

**Error: "No module named openpyxl"**
```bash
python -m pip install openpyxl
```

**Error: "No module named pandas"**
```bash
python -m pip install pandas
```

**Port 8000 already in use?**
```bash
python manage.py runserver 8001
```

**Clear Python cache:**
```bash
find . -type d -name "__pycache__" -exec rm -r {} +
```

---

### 📁 Project Structure
```
CropRecommendAndSuggesion/
├── AdminApp/          → Admin functionality
├── UserApp/           → User functionality
├── Templates/         → HTML templates
├── Static/            → CSS, JS, Images
├── Dataset/           → Training data
├── model/             → Trained ML models
├── manage.py          → Django management
├── requirements.txt   → Dependencies list
└── setup.py           → Setup checker
```

---

### 📝 First Time Setup Checklist
- [ ] Navigate to project directory
- [ ] Install all dependencies
- [ ] Run: `python manage.py migrate`
- [ ] Start server: `python manage.py runserver`
- [ ] Open: http://localhost:8000
- [ ] Login as Admin (Admin/Admin)
- [ ] Upload & preprocess dataset
- [ ] Train models
- [ ] Test via user portal

---

### 💡 Tips
- Models are pre-trained in `model/` folder
- Sample crop images should be in `cropimages/` folder
- User data stored in `cropDB.db`
- Django admin available at: http://localhost:8000/admin/

---

### ❓ Need Help?
1. Check `requirements.txt` for all dependencies
2. Run `setup.py` to verify installation
3. Check Django console output for errors
4. Ensure all data files exist in Dataset folder

Happy farming! 🚜
