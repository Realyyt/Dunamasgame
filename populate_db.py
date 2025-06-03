from src.app import app
from src.db.core import db
from src.db.models.quiz_db import Questions, Options, Answers
from src.db.models.quiz_questions import quiz_questions

with app.app_context(): 
    # Clear existing data to avoid duplicates
    db.session.query(Answers).delete()
    db.session.query(Options).delete()
    db.session.query(Questions).delete()
    db.session.commit()
    
    # Debug: Print the structure of the first question's options
    if quiz_questions:
        print(f"Question 1 structure: {quiz_questions[0]}")
        print(f"Options structure: {quiz_questions[0].get('options', 'No options found')}")
        if 'options' in quiz_questions[0]:
            first_opt = quiz_questions[0]['options'][0]
            print(f"First option type: {type(first_opt)}")
            print(f"First option content: {first_opt}")
    
    # Add each question from quiz_questions
    for i, q in enumerate(quiz_questions, start=1):
        question = Questions(question_no=i, question=q["question"])
        db.session.add(question)
        db.session.commit()  # Commit to get question_id
        
        # Add options for this question
        for j, opt in enumerate(q["options"]):
            try:
                # Try to handle different possible formats
                if isinstance(opt, dict):
                    # If it's a dictionary, look for label and text
                    label = opt.get('label', chr(65 + j))  # Default to A, B, C...
                    text = opt.get('text', str(opt))
                elif isinstance(opt, (list, tuple)) and len(opt) >= 2:
                    # If it's a list/tuple with at least 2 items
                    label = opt[0]
                    text = opt[1]
                else:
                    # Fallback: use the option as text and generate a label
                    label = chr(65 + j)  # A, B, C, ...
                    text = str(opt)
                
                option = Options(
                    question_id=question.question_id,
                    label=label,
                    text=text
                )
                db.session.add(option)
            except Exception as e:
                print(f"Error with question {i}, option {j}: {e}")
                print(f"Option data: {opt}")
                continue
        
        db.session.commit()
        
        # Add correct answer for this question
        correct_label = q.get("answer")  # Get the answer from the quiz_questions
        if correct_label:
            answer = Answers(
                question_id=question.question_id,
                correct_answer=correct_label
            )
            db.session.add(answer)
            db.session.commit()
    
    print(f"Database populated with {len(quiz_questions)} questions.")