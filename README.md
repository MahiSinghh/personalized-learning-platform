# 🚀 StudyAdda: Personalized Adaptive Learning Platform

An intelligent Flask-based ecosystem designed to identify learning gaps using **MySQL-driven analytics** and provide **automated AI-guided study recommendations**.

---

## ✨ Key Highlights
* **🧠 Weak Topic Detection:** Automatically identifies sub-topics (e.g., Python Loops, SQL Joins) where the user needs improvement.
* **📺 Smart Recommendations:** Generates dynamic YouTube tutorial links specifically for "Weak" topics to bridge knowledge gaps.
* **📉 Learning Curve Visualization:** Real-time performance tracking using **Chart.js** line graphs.
* **🛡️ Secure Industry Standards:** Password hashing with `Werkzeug` and session-based user security.
* **⏲️ Integrated Exam Timer:** JavaScript-powered countdown with auto-submit to simulate real test environments.

---

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Backend** | Python (Flask) |
| **Database** | MySQL (Relational Schema) |
| **Frontend** | HTML5, CSS3 (Glassmorphism UI), Bootstrap 5 |
| **Analytics** | Chart.js, FontAwesome Icons |
| **Environment** | VS Code, Virtualenv (.venv) |

---

## ▶️ Setup & Installation (VS Code)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-link>
   cd personalized_learning
Create & Activate Virtual Environment:

Bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate
Install Dependencies:

Bash
pip install -r requirements.txt
Environment Variables (.env):
Create a .env file in the root folder:

Code snippet
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=learning_platform
SECRET_KEY=generate_a_random_string
Database Initialization:
Import the database.sql file into your MySQL Workbench to set up tables and sample questions.

Run Application:

Bash
python app.py
Access at: http://127.0.0.1:5000

📊 Future Roadmap
🤖 AI-Driven Question Engine: Integrate Gemini/OpenAI API to generate adaptive questions that change difficulty based on the user's real-time performance.

🖥️ VS Code Extension: Develop a dedicated VS Code Sidebar Extension allowing students to take quick "Coding Concept Checks" without leaving their editor.

🔍 Contextual Deep-Link Discovery: Use AI to map specific wrong answers to exact timestamps in educational videos for pinpoint learning.

🏆 Peer-to-Peer Challenges: A global leaderboard and 1v1 "Quiz Battles" to gamify the learning experience.

📜 Verified Skill Badges: Automated PDF certificate generation for users reaching "Advanced" status in specific domains.

👩‍💻 Developed By
Mahi Singh