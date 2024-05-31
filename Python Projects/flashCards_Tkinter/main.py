import tkinter
from tkinter import *
import pandas
import pandas as pd
import random

# Checking for file and reading for enToBg or wordsToLearn file---------------------------------------------------------
try:
    df = pd.read_csv("wordsToLearn.csv")
    to_learn = df.to_dict(orient="records")
except FileNotFoundError:
    df = pd.read_csv("enToBg.csv")
    to_learn = df.to_dict(orient="records")

# Global variables------------------------------------------------------------------------------------------------------
rand_word = ""
rand_pair = {}

# Languages-------------------------------------------------------------------------------------------------------------
languages_list = df.columns.tolist()

# Consts----------------------------------------------------------------------------------------------------------------
WINDOW_X = 560
WINDOW_Y = 380

# Creating window-------------------------------------------------------------------------------------------------------
window = Tk()
window.title("Flash cards")
window.resizable(False, False)


def yes_button_():
    global to_learn

    to_learn.remove(rand_pair)
    temp_date = pandas.DataFrame(to_learn)
    temp_date.to_csv("wordsToLearn.csv", index=False)

    unknown_side()


def no_button_():
    unknown_side()


def unknown_side():
    yes_button.config(state=DISABLED)
    no_button.config(state=DISABLED)

    global rand_pair
    global rand_word
    global to_learn

    rand_pair = random.choice(to_learn)
    rand_word = rand_pair[languages_list[0]]
    canvas.itemconfig(language_box, text=languages_list[0])
    canvas.itemconfig(word_box, text=rand_word)

    window.after(3000, func=known_side)


def known_side():
    yes_button.config(state=NORMAL)
    no_button.config(state=NORMAL)

    canvas.itemconfig(language_box, text=languages_list[1])
    canvas.itemconfig(word_box, text=rand_pair[languages_list[1]])


# Creating canvas-------------------------------------------------------------------------------------------------------
canvas = Canvas(width=WINDOW_X, height=WINDOW_Y)
image = PhotoImage(file="note.png")
canvas.create_image(WINDOW_X / 2, WINDOW_Y / 2, image=image)
canvas.grid(row=0, column=0)

# Text boxes------------------------------------------------------------------------------------------------------------
text_x_offset = WINDOW_X / 2
text_y_offset = WINDOW_Y / 2

# Language box
language_box = canvas.create_text(text_x_offset, text_y_offset - 150, text=languages_list[0], font=("Arial", 15, "bold"))

# Word box
word_box = canvas.create_text(text_x_offset, text_y_offset - 50, text=languages_list[1], font=("Arial", 15, "italic"))

# Buttons---------------------------------------------------------------------------------------------------------------
button_x_offset = (WINDOW_X / 2) / 2
button_y_offset = 110

# Yes button position
yes_button_x = (WINDOW_X / 2) - button_x_offset
yes_button_y = (WINDOW_Y / 2) + button_y_offset

# Yes button config
yes_button = tkinter.Button(text="Yes", width=4, height=2, bg="WHITE", command=yes_button_)
yes_button.place(x=yes_button_x, y=yes_button_y)

# - #

# No button position
no_button_x = (WINDOW_X / 2) + button_x_offset
no_button_y = (WINDOW_Y / 2) + button_y_offset

# No button config
no_button = tkinter.Button(text="No", width=4, height=2, bg="WHITE", command=no_button_)
no_button.place(x=no_button_x, y=no_button_y)

unknown_side()
window.mainloop()
