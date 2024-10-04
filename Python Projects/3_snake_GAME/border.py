from turtle import Turtle


class Border(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("square")
        self.color("red")
        self.shapesize(1)
        self.hideturtle()
        self.penup()
        self.goto(-170, -170)

    def draw_border(self):
        self.pendown()
        self.goto(170, -170)
        self.goto(170, 170)
        self.goto(-170, 170)
        self.goto(-170, -170)
