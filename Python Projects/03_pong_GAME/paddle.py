from turtle import Turtle


class Paddle(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.speed("fast")
        self.shape("square")
        self.color("white")
        self.shapesize(2, 0.5)
        self.penup()
        self.goto(x, y)

    def move_up(self):
        if self.ycor() < 260:
            self.sety(self.ycor() + 35)

    def move_down(self):
        if self.ycor() > -260:
            self.sety(self.ycor() - 35)

