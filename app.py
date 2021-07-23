from flask import Flask, render_template, request, redirect, flash

from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False

@app.route('/')
def start_page():
    survey_obj = satisfaction_survey
    return render_template('start.html', survey_obj=survey_obj)

@app.route('/questions/<num>')
def questions(num):
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank_you')
    if int(num) != len(responses)+1:
    
        flash("You are trying to access an invalid question!")

        proper_num = len(responses)+1
        return redirect (f"/questions/{proper_num}")
    curr_question = satisfaction_survey.questions[int(num)-1]
    question = curr_question.question
    choices = curr_question.choices
    return render_template('questions.html', num=num, question=question, choices=choices)

@app.route('/answer/<num>', methods=["POST"])
def answer(num):
    button_answer = request.form["button"]
    responses.append(button_answer)
    next_q = int(num)+1
    print(responses)
    if next_q > len(satisfaction_survey.questions):
        return redirect("/thank_you")
    else:
        return redirect(f"/questions/{next_q}")

@app.route('/thank_you')
def thank_you():
    print(responses)
    return render_template('thank_you.html')