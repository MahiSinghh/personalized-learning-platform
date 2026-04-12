import os
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback_secret")

# Database connection helper
def get_db():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Results ko dictionary ki tarah access karne ke liye
    return conn

db = get_db()
cursor = db.cursor()

# Updated Table Schema (Added email and password for Login/Signup)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    score INTEGER DEFAULT 0
)
""")
db.commit()

# Helper Function: Generate YouTube Links
def get_youtube_link(topic):
    search_query = topic.replace(" ", "+") + "+tutorial"
    return f"https://www.youtube.com/results?search_query={search_query}"


# =========================
# REGISTER ROUTE
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not name or not email or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        
        # SQLite Connection (Local thread safety ke liye har baar fetch karein)
        local_db = get_db()
        local_cursor = local_db.cursor()

        # Check if email already exists in 'users' table (NOT 'students')
        local_cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = local_cursor.fetchone()

        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))

        # Insert into 'users' table using '?' placeholders
        try:
            local_cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )
            local_db.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error: {e}")
            flash("An error occurred during registration.", "danger")
            return redirect(url_for('register'))

    return render_template("register.html")

# HOME ROUTE
@app.route('/')
def home():
    return render_template("index.html")



# =========================
# LOGIN ROUTE
# =========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        local_db = get_db()
        local_cursor = local_db.cursor()

        # Query updated: 'users' table and '?' placeholder
        local_cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = local_cursor.fetchone()

        # user[3] password hai, user[0] id, user[1] username
        if user and check_password_hash(user['password'], password):
            session['student_id'] = user['id']
            session['name'] = user['username']
            session['user'] = user['email']
            
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for('quiz'))
        else:
            flash("Invalid email or password!", "danger")
            return redirect(url_for('login'))

    return render_template("login.html")
# =========================
# QUIZ ROUTE (Fixed for SQLite)
# =========================
@app.route('/quiz')
def quiz():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    local_db = get_db()
    local_cursor = local_db.cursor()

    # Fixed: RANDOM() instead of RAND()
    local_cursor.execute("""
        SELECT id, question, option_a, option_b, option_c, option_d, topic, correct_option
        FROM questions
        ORDER BY RANDOM()
        LIMIT 5
    """)
    quiz_questions = local_cursor.fetchall()
    
    quiz_meta = {}
    questions_for_frontend = []

    for q in quiz_questions:
        # q['id'] use kar rahe hain kyunki Row_factory enabled hai
        quiz_meta[str(q['id'])] = {'correct': q['correct_option'].strip().lower(), 'topic': q['topic']}
        questions_for_frontend.append(q)

    session['quiz_meta'] = quiz_meta
    return render_template("quiz.html", questions=questions_for_frontend)

# =========================
# SUBMIT ROUTE (Fixed for SQLite)
# =========================
@app.route('/submit', methods=['POST'])
def submit():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    student_id = session.get('student_id')
    quiz_meta = session.get('quiz_meta', {})
    
    if not quiz_meta:
        return redirect(url_for('quiz'))

    local_db = get_db()
    local_cursor = local_db.cursor()

    score = 0
    results = []
    topic_stats = {}

    for q_id, meta in quiz_meta.items():
        selected = request.form.get(f'q{q_id}', '').strip().lower()
        correct = meta['correct']
        topic = meta['topic']

        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "total": 0}
        
        topic_stats[topic]["total"] += 1
        is_correct = (selected == correct)

        if is_correct:
            score += 1
            topic_stats[topic]["correct"] += 1

        # Fixed: ? placeholder
        local_cursor.execute("SELECT question, option_a, option_b, option_c, option_d FROM questions WHERE id = ?", (q_id,))
        q_data = local_cursor.fetchone()
        
        opt_map = {'a': q_data['option_a'], 'b': q_data['option_b'], 'c': q_data['option_c'], 'd': q_data['option_d']}

        results.append({
            "question": q_data['question'],
            "selected": opt_map.get(selected, "Not Answered"),
            "correct": opt_map.get(correct),
            "is_correct": is_correct
        })

    total = len(quiz_meta)
    level = "Beginner" if score <= total*0.4 else "Intermediate" if score <= total*0.7 else "Advanced"
    
    # Fixed: ? placeholders and Ensure 'results' table exists
    local_cursor.execute("INSERT INTO results (score, level, student_id) VALUES (?, ?, ?)", (score, level, student_id))
    local_db.commit()

    local_cursor.execute("SELECT score, level FROM results WHERE student_id = ? ORDER BY id ASC", (student_id,))
    history = local_cursor.fetchall()
    scores = [row['score'] for row in history]
    average = round(sum(scores)/len(scores), 2) if scores else 0

    # Recommendation Logic
    topic_performance = {}
    recommendations = []

    for topic, data in topic_stats.items():
        accuracy = (data["correct"] / data["total"]) * 100
        if accuracy >= 75: tag, status = "Strong ✔️", "success"
        elif accuracy >= 50: tag, status = "Average ⚠️", "warning"
        else:
            tag, status = "Weak ❌", "danger"
            recommendations.append({"topic": topic, "link": get_youtube_link(topic)})

        topic_performance[topic] = {"accuracy": round(accuracy, 2), "level": tag, "status": status}

    return render_template(
        "result.html",
        score=score, total=total, level=level,
        history=history[::-1], average=average,
        results=results, scores=scores,
        topic_performance=topic_performance,
        recommendations=recommendations
    )

# =========================

# LOGOUT

# =========================

@app.route('/logout')

def logout():

    session.clear()

    return redirect(url_for('login'))





if __name__ == '__main__':

    app.run(debug=True)

