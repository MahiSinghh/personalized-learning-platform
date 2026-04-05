# 🚀 StudyAdda — Personalized Adaptive Learning Platform  

An intelligent **Flask-based learning system** that analyzes user performance, identifies weak areas, and delivers **data-driven personalized learning recommendations** to improve outcomes efficiently.  

---

## 🌟 Overview  

StudyAdda is designed to move beyond traditional quiz platforms by introducing **adaptive learning techniques**.  
It tracks user performance at a granular level and transforms insights into **actionable learning suggestions**.

---

## ✨ Core Features  

### 🧠 Smart Weak Topic Detection  
- Identifies performance at **topic & sub-topic level**  
- Highlights weak areas like *Loops, Arrays, SQL Joins*  
- Helps users focus only where improvement is needed  

### 📺 AI-Guided Learning Recommendations  
- Generates **targeted YouTube resources** for weak topics  
- Reduces time spent searching for the right content  

### 📊 Performance Analytics Dashboard  
- Visualizes progress using **Chart.js graphs**  
- Tracks score trends and learning curve over time  

### ⏲️ Real Exam Simulation  
- Built-in **quiz timer with auto-submit**  
- Mimics real exam pressure environment  

### 🔐 Secure Authentication System  
- Password hashing using `Werkzeug`  
- Session-based login system  

---

## 🛠️ Tech Stack  

| Layer        | Technology Used |
|-------------|----------------|
| **Backend** | Python (Flask) |
| **Database** | MySQL |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **UI Design** | Glassmorphism + Responsive Design |
| **Analytics** | Chart.js |
| **Tools** | VS Code, Virtual Environment |

---

## ⚙️ Setup & Installation  

### 1️⃣ Clone Repository  
```bash
git clone <your-repo-link>
cd personalized_learning
```

### 2️⃣ Create Virtual Environment  
```bash
python -m venv .venv
```

### 3️⃣ Activate Environment  

**Windows**
```bash
.venv\Scripts\activate
```

**Mac/Linux**
```bash
source .venv/bin/activate
```

### 4️⃣ Install Dependencies  
```bash
pip install -r requirements.txt
```

### 5️⃣ Configure Environment Variables  

Create a `.env` file in root directory:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=learning_platform
SECRET_KEY=your_secret_key
```

### 6️⃣ Setup Database  
- Import `database.sql` into MySQL  
- This will create tables and insert sample quiz data  

### 7️⃣ Run Application  
```bash
python app.py
```

👉 Open in browser:  
http://127.0.0.1:5000

---

## 📈 Future Enhancements  

- 🤖 AI Question Generator (Gemini / OpenAI integration)  
- 🎯 Adaptive Difficulty System  
- 📚 Subject-wise Quiz Modules  
- 🔗 YouTube Timestamp Recommendations  
- 🏆 Leaderboard & Competitive Mode  
- 📜 Auto Certificate Generation  

---

## 💡 Key Learning Outcomes  

- Built a **full-stack data-driven application**  
- Implemented **performance analytics & tracking**  
- Designed **adaptive learning logic**  
- Integrated **secure authentication system**  

---
## 👩‍💻 Author  

**Mahi Singh**    

---

## ⭐ Support  

If you found this project useful, consider giving it a ⭐ on GitHub!