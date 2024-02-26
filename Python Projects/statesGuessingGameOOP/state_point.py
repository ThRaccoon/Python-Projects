from turtle import Turtle


class StatePoint(Turtle):
    def __init__(self, name, x, y):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.name = name
        self.x = x
        self.y = y
        point = Turtle()
        point.penup()
        point.shape("circle")
        point.shapesize(0.2)
        point.color("red")
        point.goto(x, y)
        self.write_state()

    def write_state(self):
        self.goto(self.x, self.y)
        self.write(self.name, False, "left", ("Verdana", 7, "normal"))

