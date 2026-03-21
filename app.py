from dotenv import load_dotenv
import os

load_dotenv()

from flask import flash
import mysql.connector
from flask import Flask, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
# from quiz_data import questions

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = db.cursor()


# =========================
# REGISTER ROUTE
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = generate_password_hash(password)

        # Check if email already exists
        cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))


        cursor.execute(
            "INSERT INTO students (name, email, password) VALUES (%s, %s, %s)",
            (name, email, hashed_password)
        )
        db.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template("register.html")


# =========================
# LOGIN ROUTE
# =========================
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        cursor.execute("SELECT * FROM students WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['student_id'] = user[0]
            session['name'] = user[1]
            return redirect(url_for('quiz'))
        else:
            flash("Invalid email or password!", "danger")
            return redirect(url_for('login'))


    return render_template("login.html")


# =========================
# QUIZ ROUTE
# =========================
@app.route('/quiz')
def quiz():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    # ✅ Fetch random 5 questions from DB
    cursor.execute("""
        SELECT id, question, option_a, option_b, option_c, option_d
        FROM questions
        ORDER BY RAND()
        LIMIT 5
    """)
    
    quiz_questions = cursor.fetchall()

    # ✅ Store question IDs in session
    session['quiz_questions'] = [q[0] for q in quiz_questions]

    # ✅ Send to frontend
    return render_template("quiz.html", questions=quiz_questions)


# =========================
# SUBMIT ROUTE
# =========================
@app.route('/submit', methods=['POST'])
def submit():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    student_id = session.get('student_id')

    # Get quiz question IDs from session
    question_ids = session.get('quiz_questions', [])

    if not question_ids:
        return redirect(url_for('quiz'))

    score = 0
    results = []

    # Loop through each question
    for question_id in question_ids:
        selected_answer = request.form.get(f'q{question_id}')

        cursor.execute("""
            SELECT question, option_a, option_b, option_c, option_d, correct_option 
            FROM questions WHERE id=%s
        """, (question_id,))
        
        q_data = cursor.fetchone()

        question_text = q_data[0]
        options = {
            'a': q_data[1],
            'b': q_data[2],
            'c': q_data[3],
            'd': q_data[4]
        }
        correct_answer = q_data[5]

        is_correct = selected_answer == correct_answer

        if is_correct:
            score += 1

        results.append({
            "question": question_text,
            "selected": options.get(selected_answer, "Not Answered"),
            "correct": options[correct_answer],
            "is_correct": is_correct
        })

    total = len(question_ids)

    # ✅ Dynamic Level Calculation
    if score <= total * 0.4:
        level = "Beginner"
    elif score <= total * 0.7:
        level = "Intermediate"
    else:
        level = "Advanced"

    # ✅ Feedback Message
    if level == "Beginner":
        message = "Revise basic concepts and practice more."
    elif level == "Intermediate":
        message = "Good progress! Try moderate difficulty questions."
    else:
        message = "Excellent performance! Try advanced challenges."

    # ✅ Store result in DB
    sql = "INSERT INTO results (score, level, student_id) VALUES (%s, %s, %s)"
    cursor.execute(sql, (score, level, student_id))
    db.commit()

    # ✅ Fetch history
    cursor.execute("""
        SELECT score, level 
        FROM results 
        WHERE student_id=%s 
        ORDER BY attempt_date ASC
    """, (student_id,))
    
    history = cursor.fetchall()

    scores = [row[0] for row in history]

    # ✅ Average calculation
    average = round(sum(scores) / len(scores), 2) if scores else 0

    # ✅ Improvement detection
    improvement_message = ""
    status = "neutral"

    if len(scores) >= 2:
        latest = scores[-1]
        previous = scores[-2]

        if latest > previous:
            improvement_message = "Great! Your performance is improving 📈"
            status = "improve"
        elif latest < previous:
            improvement_message = "Your performance decreased. Revise and try again 📉"
            status = "decrease"
        else:
            improvement_message = "Your performance is consistent."
            status = "neutral"

    # ✅ Final render
    return render_template(
        "result.html",
        score=score,
        total=total,
        level=level,
        message=message,
        history=history,
        average=average,
        improvement_message=improvement_message,
        status=status,
        results=results,
        scores=scores
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


