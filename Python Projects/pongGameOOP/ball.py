from turtle import Turtle
import random


directions = (35, 145, 215, 325)
direction = random.choice(directions)


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.speed("fastest")
        self.shape("circle")
        self.color("white")
        self.shapesize(1, 1)
        self.penup()
        self.goto(0, 0)
        self.x_move = 15
        self.y_move = 15
        self.direction = direction

    def start_move(self):   # up left 145, up right 35, down right 325, down left 215
        self.setheading(self.direction)
        self.forward(15)

    def move(self):
        x = self.xcor() + self.x_move
        y = self.ycor() + self.y_move
        self.goto(x, y)

    def bounce_x(self):
        self.x_move *= -1

    def bounce_y(self):
        self.y_move *= -1

    def reset_ball(self):
        self.goto(0, 0)
        self.direction = random.choice(directions)
        self.start_move()
