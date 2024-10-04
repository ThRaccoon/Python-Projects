from turtle import Turtle


class Food(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.shape("circle")
        self.color("blue")
        self.shapesize(0.8)
        self.penup()
        self.goto(self.x, self.y)

    def del_food(self):
        self.hideturtle()
