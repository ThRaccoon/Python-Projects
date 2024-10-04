from turtle import Turtle


class Border(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("red")
        self.hideturtle()
        self.shapesize(1, 0.5)
        self.penup()
        self.goto(-455, -350)

    def draw_border(self):
        self.pendown()
        self.goto(455, -350)
        self.goto(455, 350)
        self.goto(-455, 350)
        self.goto(-455, -350)
