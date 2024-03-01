import json
import random

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from starlette.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")

with open('questions.json', 'r') as file:
    data = json.load(file)
    questions = data['questions']


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "total_questions": len(questions)})


@app.get("/quiz", response_class=HTMLResponse)
async def read_quiz(request: Request, num_questions: int = 5):
    selected_questions = random.sample(questions, k=min(num_questions, len(questions)))
    return templates.TemplateResponse("quiz.html", {"request": request, "questions": selected_questions})


@app.post("/results", response_class=HTMLResponse)
async def show_results(request: Request):
    form_data = await request.form()
    correct = 0
    answered = 0  # Number of questions answered
    wrong_answers = []

    for question_number, user_answer in form_data.items():
        answered += 1
        actual_question = next((q for q in questions if str(q['number']) == question_number.split('_')[-1]), None)
        if actual_question and (str(actual_question['answer']) == user_answer):
            correct += 1
        elif actual_question:
            wrong_answers.append({'number': actual_question['number'], 'question': actual_question['question'], 'answer': actual_question['answer'], 'user_answer': user_answer == 'True'})

    percentage = round((correct / answered) * 100, 2) if answered else 0

    return templates.TemplateResponse("results.html", {"request": request, "correct": correct, "answered": answered, "percentage": percentage, "wrong_answers": wrong_answers})


