# 🚀 How to Run Crop Recommendation Project in VS Code

## 📋 Prerequisites
- VS Code installed
- Python 3.x installed
- Project folder downloaded

---

## ⚡ Step 1: Open Project in VS Code

1. **Open VS Code**
2. Click **File → Open Folder**
3. Navigate to: `c:\Users\tamid\Downloads\CropRecommendAndSuggesion\CropRecommendAndSuggesion`
4. Click **Select Folder**

---

## ⚡ Step 2: Install Recommended VS Code Extensions

Press `Ctrl + X` (Extensions) and install:

| Extension | Publisher | Purpose |
|-----------|-----------|---------|
| **Python** | Microsoft | Python language support |
| **Pylance** | Microsoft | Python intellisense |
| **Django** | Baptiste Darthenay | Django template support |
| **Thunder Client** | Rangav | API testing (optional) |
| **Better Comments** | Aaron Bond | Code commenting (optional) |

**Quick Install:**
1. Press `Ctrl + Shift + X`
2. Search: `python`
3. Click Install

---

## ⚡ Step 3: Configure Python Environment

### **Method A: Auto-Detection (Recommended)**

1. Press `Ctrl + Shift + P` (Command Palette)
2. Type: `Python: Select Interpreter`
3. Choose the Python interpreter (should show version)
4. VS Code will recognize the environment automatically

### **Method B: Manual Configuration**

1. Go to **File → Preferences → Settings**
2. Search: `python.defaultInterpreterPath`
3. Set to your Python executable:
   ```
   c:\Users\tamid\AppData\Local\Programs\Python\Python3x\python.exe
   ```

---

## ⚡ Step 4: Open Integrated Terminal

**Press** `Ctrl + `` ` (Backtick)

Or: **View → Terminal**

You should see terminal at bottom of VS Code

---

## ⚡ Step 5: Install Dependencies

In the integrated terminal, type:

```bash
python -m pip install -r requirements.txt
```

Or use the setup script:

```bash
python setup.py
```

**Wait for completion** ✓

---

## ⚡ Step 6: Apply Database Migrations

```bash
python manage.py migrate
```

---

## ⚡ Step 7: Run Django Server

```bash
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
```

---

## ⚡ Step 8: Access the Application

**In your browser, open:**
- Main: http://localhost:8000
- Admin Login: http://localhost:8000
- User Login: http://localhost:8000/userapp/login

---

## 🎯 VS Code Tips & Tricks

### **1. Stop the Server**
- Press `Ctrl + C` in terminal
- Or click X on terminal tab

### **2. Restart Server**
- Press `Ctrl + C`
- Run command again: `python manage.py runserver`

### **3. View File Structure**
- Press `Ctrl + B` to toggle Explorer sidebar
- View: AdminApp, UserApp, Templates, Dataset folders

### **4. Open File Quickly**
- Press `Ctrl + P`
- Type filename: `views.py`, `models.py`, etc.

### **5. Debug Django**

Create `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["runserver"],
            "django": true,
            "justMyCode": true
        }
    ]
}
```

Then press `F5` to debug!

### **6. Format Code**
- Press `Shift + Alt + F` to auto-format
- Configure in Settings if needed

### **7. Search Files**
- Press `Ctrl + Shift + F`
- Search across entire project
- Perfect for finding functions!

---

## 📁 Project Files to Know

| File | Purpose | Open with |
|------|---------|-----------|
| `manage.py` | Django management | Terminal |
| `UserApp/views.py` | User functions | Click to edit |
| `AdminApp/views.py` | Admin functions | Click to edit |
| `requirements.txt` | Dependencies | View only |
| `TEST_DATA_GUIDE.md` | Test cases | Click to read |

---

## 🔧 Common Tasks in VS Code

### **Task 1: Edit a View Function**

1. Press `Ctrl + Shift + F`
2. Search: `def CropAction`
3. Click result
4. Edit code
5. Save: `Ctrl + S`
6. Server auto-reloads!

### **Task 2: Run Scripts**

```bash
# Retrain models
python retrain_models.py

# Add test users
python insert_sample_users.py

# Run manage.py commands
python manage.py migrate
python manage.py runserver
```

### **Task 3: View Logs**

Scroll up in terminal to see:
- Django startup messages
- Request logs
- Error messages

### **Task 4: Stop and Clear**

```bash
# Clear terminal
cls

# Stop server
Ctrl + C

# Start fresh
python manage.py runserver
```

---

## 🐛 Troubleshooting in VS Code

### **Problem: "Python not found"**
- Press `Ctrl + Shift + P`
- Type: `Python: Select Interpreter`
- Choose correct Python version

### **Problem: "Module not found"**
```bash
# Reinstall dependencies
python -m pip install -r requirements.txt
```

### **Problem: Port 8000 in use**
```bash
# Use different port
python manage.py runserver 8001
```

### **Problem: Server won't start**
1. Check terminal for errors
2. Press `Ctrl + C` to stop
3. Try: `python manage.py migrate`
4. Restart: `python manage.py runserver`

---

## 💡 VS Code Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + B` | Toggle sidebar |
| `Ctrl + `` ` | Toggle terminal |
| `Ctrl + P` | Open file quick search |
| `Ctrl + Shift + F` | Search in files |
| `Ctrl + S` | Save file |
| `Ctrl + /` | Toggle comment |
| `Alt + ↑/↓` | Move line up/down |
| `Ctrl + D` | Select next match |
| `F5` | Start debugging |
| `Ctrl + C` | Stop terminal command |

---

## ✅ Quick Start Checklist

- [ ] Open project in VS Code
- [ ] Install Python extension
- [ ] Select Python interpreter (Ctrl + Shift + P)
- [ ] Open terminal (Ctrl + `` `)
- [ ] Install dependencies: `python -m pip install -r requirements.txt`
- [ ] Apply migrations: `python manage.py migrate`
- [ ] Run server: `python manage.py runserver`
- [ ] Open: http://localhost:8000
- [ ] Login with Admin/Admin or rajesh/pass123
- [ ] Test features!

---

## 📊 VS Code Layout Suggestion

```
┌─────────────────────────────────────────┐
│  📁 Explorer      🔍 Search    ⚙️ Debug │
├─────────────────────────────────────────┤
│                                         │
│  AdminApp/          │  views.py         │
│  UserApp/           │  (Editing area)   │
│  Templates/         │                   │
│  Dataset/           │                   │
│  model/             │                   │
│  manage.py          │                   │
│                                         │
├─────────────────────────────────────────┤
│ > python manage.py runserver            │
│ Starting development server at 8000/    │
└─────────────────────────────────────────┘
```

---

## 🎓 Learning Resources

- **Django Docs:** https://docs.djangoproject.com/
- **Python Docs:** https://docs.python.org/3/
- **VS Code Docs:** https://code.visualstudio.com/docs
- **scikit-learn:** https://scikit-learn.org/

---

## ✨ You're All Set!

You can now:
- ✅ Edit code in VS Code
- ✅ See real-time errors
- ✅ Run Django server
- ✅ Test the application
- ✅ Debug issues with F5

**Happy coding!** 🚀
