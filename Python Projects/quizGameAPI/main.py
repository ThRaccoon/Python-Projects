import quiz_logic
import quiz_UI
import requests
from tkinter import *


# Global variables------------------------------------------------------------------------------------------------------
URL = "https://opentdb.com/api.php?amount=10&type=boolean"
request = requests.get(URL)
data = request.json()


# Main window-----------------------------------------------------------------------------------------------------------
window = Tk()
window.title("Quiz Games")
window.config(padx=10, pady=10, background="White")
window.resizable(False, False)


# Formating the questions and answers-----------------------------------------------------------------------------------
def fill_dict(_data):
    _list_of_questions_and_answers = []
    for result in range(10):
        _q_and_a = _data['results'][result]
        _dict = {'question': _q_and_a['question'], 'answer': _q_and_a['correct_answer']}
        _list_of_questions_and_answers.append(_dict)
    return _list_of_questions_and_answers


list_of_q_and_a = fill_dict(data)
print(list_of_q_and_a)


# Quiz logic------------------------------------------------------------------------------------------------------------
ql = quiz_logic.QuizLogic(list_of_q_and_a)
# Quiz UI---------------------------------------------------------------------------------------------------------------
qui = quiz_UI.QuizUI()


# Functions-------------------------------------------------------------------------------------------------------------
def start():
    qui.delete_main_menu()

    window.after(100, create)


def create():
    qui.create_question_text_box()
    qui.create_guessed_questions_score()
    qui.create_current_question_number()
    qui.create_true_button(true_button)
    qui.create_false_button(false_button)

    question_text = ql.question_text()
    qui.update_question_text_box(question_text)


def next_question():
    qui.enb_true_button()
    qui.enb_false_button()

    current_question = ql.update_current_question()
    qui.update_current_question_number(current_question)

    qui.change_question_text_box_color("White")

    next_question_text = ql.question_text()
    qui.update_question_text_box(next_question_text)


def true_button():
    check = ql.check_user_answer(user_answer="True")

    qui.update_guessed_questions_score(check[0])
    qui.change_question_text_box_color(check[1])

    qui.dis_true_button()
    qui.dis_false_button()

    ql.next_question()
    if ql.counter == 10:
        window.after(500, end_scene)
    else:
        window.after(1000, next_question)


def false_button():
    check = ql.check_user_answer(user_answer="False")

    qui.update_guessed_questions_score(check[0])
    qui.change_question_text_box_color(check[1])

    qui.dis_true_button()
    qui.dis_false_button()

    ql.next_question()
    if ql.counter == 10:
        window.after(500, end_scene)
    else:
        window.after(1000, next_question)


def end_scene():
    qui.delete_gameplay_scene()
    qui.create_end_scene(ql.guessed_questions, ql.current_question, exit_button)


def exit_button():
    exit(0)


# Starts here-----------------------------------------------------------------------------------------------------------
qui.create_main_menu(start)


window.mainloop()
