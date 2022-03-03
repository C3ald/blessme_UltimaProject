import random
from flask import Flask, redirect, url_for, render_template, request, session, flash
from pydantic.types import NoneBytes
from tinydb import TinyDB

app = Flask(__name__) #Import this
DB = TinyDB('questions.json')
NUM_ = TinyDB('num_of_questions.json')

global QUESTIONS
global qs
QUESTIONS = [{'question': 'Who is the narrator of the story?', 'answer':'Antonio'},
	     {'question': "What is the 'god' mentioned in the story (Not God)?", 'answer': 'The Golden Carp'},
	     {'question': 'How old was Antonio when Ultima starts to live with the family', 'answer':'almost seven'},
	     {'question': 'Where does the story mainly take place?', 'answer': 'New Mexico'},
	     {'question': "What was Ultima's occupation?", 'answer': 'natural healer'},
	     {'question': "What was Ultima's pet that she brought with her?", 'answer': 'Owl' or 'An owl'},
	     {'question': "What happend to Antonio after he graduated first grade?", 'answer': "He got promoted to third grade"},
	     {'question': "What illness did Antonio get after he saw the murder?", 'answer': "Pneumonia"},
	     {'question': "What occurred in the town later in the summer?", 'answer': "Tenorio's daughter died"},
	     {'question': "What did Antonio realize about Ultima's owl?", 'answer': "It was Ultima's spirit"},]

qs = None
global START_QUIZ
global NUM_RIGHT
START_QUIZ = 0
NUM_RIGHT = 0



def pick_questions():
	global qs
	global START_QUIZ
	global NUM_RIGHT
	NUM_RIGHT = 0
	START_QUIZ = 0
	qs = []
	i = 0
	while i != 10:
		question = random.choice(QUESTIONS)
		if question not in qs:
			qs.append(question)
			i += 1
	random.shuffle(qs)
	# print(qs)
	return qs

def question_on():
	i = START_QUIZ
	data = qs
	return data[i]


def check_answer(answer:str):
	global START_QUIZ
	global NUM_RIGHT
	# print(START_QUIZ)
	questions = qs
	question = questions[START_QUIZ]
	if question['answer'] in answer:
		NUM_RIGHT += 1
	START_QUIZ += 1
	

def results():
	""" Gets the results of the quiz """
	i = NUM_RIGHT / START_QUIZ
	d = i * 100
	results = f'{d}%'
	return results




@app.route('/')
def index():
	""" Shows homepage """
	START_QUIZ = 0
	NUM_RIGHT = 0
	questions = pick_questions()
	template = render_template('index.html')
	return template

@app.route('/quiz', methods=["GET", "POST"])
def quiz():
	""" Shows question page """
	if qs != None:
		if START_QUIZ != 9:
			print(START_QUIZ)
			if request.method == "POST" and START_QUIZ != 9:
				answer = request.form['answer']
				check_answer(answer)
			template = render_template('quiz.html', question=question_on())
			return template
		else:
			template = render_template('results.html', results=results())
			return template
	else:
		template = redirect('/')
	return template

if __name__ == '__main__':
	app.run()