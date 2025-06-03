from flask import Blueprint, jsonify, request, render_template, session
from src.db.core import db
from src.db.models.quiz_db import Questions, Answers, Options, Response
import random as r

practice_bp = Blueprint('practice', __name__)
@practice_bp.route('/api/practice/questions', methods=['GET'])
def practice_view():
    return render_template('practiceQuiz.html')

@practice_bp.route('/api/practice/questions/submit', methods=['GET', 'POST'])
def practice_question():
    '''view practice questions'''
    if request.method == 'GET':
        # fetch random questions 1-70 from the database
        all_questions = Questions.query.filter(Questions.question_no.between(1, 70)).all()
        practice_questions = r.sample(all_questions, len(all_questions))
        question_ids = [q.question_id for q in practice_questions]
        all_correct_answers = {a.question_id: a.correct_answer for a in Answers.query.filter(Answers.question_id.in_(question_ids)).all()}
        if not practice_questions:
            return jsonify({'error': 'No practice questions found'}), 404
        
        result = []
        for question in practice_questions:
            # get options for each question
            options = Options.query.filter_by(question_id=question.question_id).all()
            options_list =[{'label': opt.label, 'text': opt.text} for opt in options]
            question_data = {
                'question_no': question.question_no,
                'question': question.question,
                'options': options_list
            }
            result.append(question_data)
        
        return jsonify(result), 200
        
    elif request.method == 'POST':
        # for practice submission
        data = request.get_json()
        user_answers = data.get('answers', {})
        
        # Get all questions for the practice
        all_questions = Questions.query.filter(Questions.question_no.between(1, 70)).all()
        total_questions = len(all_questions)
        score = 0 
        results = []

        # loop through all questions
        for question_no in range(1, 71):
            question = Questions.query.filter_by(question_no=question_no).first()
            if not question:
                continue
                
            # get correct answer
            correct_answer = Answers.query.filter_by(question_id=question.question_id).first()
            user_ans = user_answers.get(str(question_no))
            
            # Convert both answers to lowercase and strip whitespace
            user_ans_clean = user_ans.strip().lower() if user_ans else None
            correct_ans_clean = correct_answer.correct_answer.strip().lower() if correct_answer else None
            is_correct = (user_ans_clean == correct_ans_clean)
            
            if is_correct:
                score += 1
                
            results.append({
                "question_no": question_no,
                "question": question.question,
                "user_answer": user_ans,
                "correct_answer": correct_answer.correct_answer if correct_answer else None,
                "is_correct": is_correct
            })

        return jsonify({
            "score": score,
            "total": total_questions,
            "percentage": (score / total_questions) * 100 if total_questions > 0 else 0,
            "results": results
        }), 200