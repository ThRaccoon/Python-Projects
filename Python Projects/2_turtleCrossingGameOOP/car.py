from turtle import Turtle
import random


class Car(Turtle):
    def __init__(self, car_weight, car_height, screen_weight, screen_height, offset):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.goto(400, 400)
        self.car = Turtle()
        self.car.penup()
        self.car.left(90)
        self.car.shape("square")
        self.car_color()
        self.car.shapesize(car_weight, car_height)
        self.car.left(90)
        self.car.teleport((screen_weight / 2) - 50, (screen_height / 2) - offset)

    def car_color(self):
        list_of_colors = ("blue", "red", "yellow", "orange", "pink", "purple", "brown", "black")
        color = random.choice(list_of_colors)
        self.car.color(color)

    def car_move(self):
        self.car.forward(20)

    def car_x_cor(self):
        return round(self.car.xcor())

    def car_y_cor(self):
        return round(self.car.ycor())
