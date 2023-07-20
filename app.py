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





