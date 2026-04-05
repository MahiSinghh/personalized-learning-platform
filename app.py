# ... (Top imports same rahenge) ...

# Helper Function: Generate YouTube Links
def get_youtube_link(topic):
    # Simple search link generator
    search_query = topic.replace(" ", "+") + "+tutorial"
    return f"https://www.youtube.com/results?search_query={search_query}"

# =========================
# QUIZ ROUTE (Updated)
# =========================
@app.route('/quiz')
def quiz():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    # ✅ Added 'topic' and 'correct_option' in the query
    cursor.execute("""
        SELECT id, question, option_a, option_b, option_c, option_d, topic, correct_option
        FROM questions
        ORDER BY RAND()
        LIMIT 5
    """)
    quiz_questions = cursor.fetchall()
    
    # Store full question data in session to avoid multiple DB calls during submit
    # Format: { id: { 'correct': 'a', 'topic': 'loops' }, ... }
    quiz_meta = {}
    questions_for_frontend = []

    for q in quiz_questions:
        quiz_meta[str(q[0])] = {'correct': q[7].strip().lower(), 'topic': q[6]}
        questions_for_frontend.append(q)

    session['quiz_meta'] = quiz_meta
    session['quiz_question_ids'] = list(quiz_meta.keys())

    return render_template("quiz.html", questions=questions_for_frontend)

# =========================
# SUBMIT ROUTE (Optimized)
# =========================
@app.route('/submit', methods=['POST'])
def submit():
    if 'student_id' not in session:
        return redirect(url_for('login'))

    student_id = session.get('student_id')
    quiz_meta = session.get('quiz_meta', {})
    
    if not quiz_meta:
        return redirect(url_for('quiz'))

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

        # Fetch question text for review
        cursor.execute("SELECT question, option_a, option_b, option_c, option_d FROM questions WHERE id=%s", (q_id,))
        q_data = cursor.fetchone()
        
        # Map letters to text
        opt_map = {'a': q_data[1], 'b': q_data[2], 'c': q_data[3], 'd': q_data[4]}

        results.append({
            "question": q_data[0],
            "selected": opt_map.get(selected, "Not Answered"),
            "correct": opt_map.get(correct),
            "is_correct": is_correct
        })

    # --- Logic for Level, History & Average (Same as yours, just keep it) ---
    total = len(quiz_meta)
    level = "Beginner" if score <= total*0.4 else "Intermediate" if score <= total*0.7 else "Advanced"
    
    cursor.execute("INSERT INTO results (score, level, student_id) VALUES (%s, %s, %s)", (score, level, student_id))
    db.commit()

    cursor.execute("SELECT score, level FROM results WHERE student_id=%s ORDER BY attempt_date ASC", (student_id,))
    history = cursor.fetchall()
    scores = [row[0] for row in history]
    average = round(sum(scores)/len(scores), 2) if scores else 0

    # ✅ SMART ANALYSIS & YOUTUBE RECOMMENDATIONS
    topic_performance = {}
    recommendations = []

    for topic, data in topic_stats.items():
        accuracy = (data["correct"] / data["total"]) * 100
        
        if accuracy >= 75:
            tag, status = "Strong ✔️", "success"
        elif accuracy >= 50:
            tag, status = "Average ⚠️", "warning"
        else:
            tag, status = "Weak ❌", "danger"
            # Add recommendation for weak topics
            recommendations.append({
                "topic": topic,
                "link": get_youtube_link(topic)
            })

        topic_performance[topic] = {
            "accuracy": round(accuracy, 2),
            "level": tag,
            "status": status
        }

    return render_template(
        "result.html",
        score=score, total=total, level=level,
        history=history[::-1], # Recent first
        average=average,
        results=results,
        scores=scores,
        topic_performance=topic_performance,
        recommendations=recommendations # Pass this to HTML!
    )