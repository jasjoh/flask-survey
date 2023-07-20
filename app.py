from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.get('/')
def survey_start():
    return render_template("survey_start.html",
        title=survey.title,
        instructions=survey.instructions
    )

@app.post("/begin")
def initial_redirect():
    return redirect("/questions/0")

@app.get("/questions/<int:qnum>")
def view_questions(qnum):
    return render_template("question.html",

        choices=survey.questions[qnum].choices,
        allow_text = survey.questions[qnum].allow_text,
        prompt=survey.questions[qnum].prompt
        )

@app.post("/answer")
def handle_answer():
    choice_picked = request.form["answer"]
    RESPONSES.append(choice_picked)
    num_of_questions = len(survey.questions)
    next_question_num = len(RESPONSES)
    print("next question number:", next_question_num)

    if (len(RESPONSES) < num_of_questions):
        return redirect(f"/questions/{next_question_num}")
    else:
        return redirect("/thankyou")

@app.get("/thankyou")
def display_thankyou():
    # RESPONSES looks like: ['Yes', 'No', 'Less than $10,000', 'Yes']
    # we want to make an array of pairs where key is question, value is answer
    # we want a list [(prompt1, answer1), (prompt2, answer2), (prompt3, answer3)]
    num_of_questions = len(survey.questions)
    range_questions = range(num_of_questions) # [0, 1, 2, 3] for 4 questions
    prompt_to_answer = []
    for index in range_questions:
        value = RESPONSES[index]
        key = survey.questions[index].prompt
        prompt_to_answer.append((key, value))
    print("prompt_to_answer:", prompt_to_answer)
    return render_template("completion.html", prompt_to_answer=prompt_to_answer)