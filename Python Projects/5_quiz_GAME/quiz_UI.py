from tkinter import *
import html


class QuizUI:
    def __init__(self):
        self.canvas = Canvas(width=460, height=200, background="White", highlightbackground="White")
        self.question_text_box = None
        self.guessed_questions = None
        self.current_question = None
        self.start_button = None
        self.true_button = None
        self.false_button = None
        self.exit_button = None
        self.text_box_img = PhotoImage(file="images/text_box_img.png")
        self.true_img = PhotoImage(file="images/true_img.png")
        self.false_img = PhotoImage(file="images/false_img.png")
        self.main_menu_img = PhotoImage(file="images/main_menu_img.png")

    # Question box------------------------------------------------------------------------------------------------------
    def create_question_text_box(self):
        self.canvas.create_image(232, 100, image=self.text_box_img)
        self.question_text_box = self.canvas.create_text(230, 100, text="N/A", width=200, font=12)
        self.canvas.grid(row=0, column=0, columnspan=2)

    def update_question_text_box(self, current_question):
        current_question = html.unescape(current_question)
        self.canvas.itemconfig(self.question_text_box, text=current_question)

    def change_question_text_box_color(self, color):
        self.canvas.config(background=color, highlightcolor=color)

    # Score box---------------------------------------------------------------------------------------------------------
    def create_guessed_questions_score(self):
        self.guessed_questions = self.canvas.create_text(405, 40, text=f"{0} ", font=10)

    def update_guessed_questions_score(self, guessed_questions):
        self.canvas.itemconfig(self.guessed_questions, text=f"{guessed_questions} ")

    def create_current_question_number(self):
        self.current_question = self.canvas.create_text(420, 40, text=f": {1}", font=10)

    def update_current_question_number(self, current_question):
        if current_question > 8:
            self.canvas.itemconfig(self.current_question, text=f":{current_question + 1}")
        else:
            self.canvas.itemconfig(self.current_question, text=f": {current_question + 1}")

    # True button-------------------------------------------------------------------------------------------------------
    def create_true_button(self, func):
        self.true_button = Button(image=self.true_img, highlightthickness=2, command=func)
        self.true_button.grid(row=1, column=0)

    def dis_true_button(self):
        self.true_button.config(state="disabled")

    def enb_true_button(self):
        self.true_button.config(state="normal")

    # False button------------------------------------------------------------------------------------------------------
    def create_false_button(self, func):
        self.false_button = Button(image=self.false_img, highlightthickness=2, command=func)
        self.false_button.grid(row=1, column=1)

    def dis_false_button(self):
        self.false_button.config(state="disabled")

    def enb_false_button(self):
        self.false_button.config(state="normal")

    # Create main menu--------------------------------------------------------------------------------------------------
    def create_main_menu(self, func):
        self.canvas.create_image(230, 100, image=self.main_menu_img)
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.start_button = Button(text="START", highlightthickness=2, command=func)
        self.start_button.grid(row=1, column=0, columnspan=2)

    # Delete main menu--------------------------------------------------------------------------------------------------
    def delete_main_menu(self):
        self.main_menu_img = None
        self.start_button.destroy()

    # Delete end screen-------------------------------------------------------------------------------------------------
    def delete_gameplay_scene(self):
        self.text_box_img = None
        self.canvas.config(background="White", highlightbackground="White")
        self.true_img = None
        self.true_button.destroy()
        self.false_img = None
        self.false_button.destroy()

    # Create end screen-------------------------------------------------------------------------------------------------
    def create_end_scene(self, guessed_questions, current_question, func):
        self.canvas.itemconfig(self.question_text_box, text="SCORE", font=60)

        self.canvas.itemconfig(self.guessed_questions, text=f"{guessed_questions} ", font=45)
        self.canvas.move(self.guessed_questions, -188, 80)

        self.canvas.itemconfig(self.current_question, text=f": {current_question + 1}", font=45)
        self.canvas.move(self.current_question, -184, 80)

        self.start_button = Button(text="EXIT", highlightthickness=2, command=func)
        self.start_button.grid(row=1, column=0, columnspan=2)
