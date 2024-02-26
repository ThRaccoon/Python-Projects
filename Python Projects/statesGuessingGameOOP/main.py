from state_point import StatePoint
from turtle import Turtle, Screen
import pandas as pd

data = pd.read_csv("states.csv")

list_of_states = data["state"].tolist()

screen = Screen()
screen.title("U.S. States")
map_png = "map.gif"
screen.addshape(map_png)

turtle = Turtle()
turtle.shape(map_png)

list_of_answers = []

number = 50

game_on = True
while game_on:

    if number > 0:
        player_answer = screen.textinput(title="Guess game", prompt=f"{number} State left!").title()
    else:
        screen.textinput(title="CONGRATZ!", prompt="Write or click OK to EXIT")
        exit()

    if player_answer in list_of_states and player_answer not in list_of_answers:
        list_of_answers.append(player_answer)
        state_info = data[data.state == player_answer]
        state_name = state_info.state.iloc[0]
        x = state_info.x.iloc[0]
        y = state_info.y.iloc[0]
        state = StatePoint(state_name, x, y)
        number -= 1
    elif player_answer in list_of_answers:
        print("This state is already guessed")
    else:
        print("Wrong Input!")
