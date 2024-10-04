from turtle import Turtle


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-170, 170)

    def draw_score(self):
        print(self.write(f"Score: {self.score}", False, "left", ("Verdana", 10, "normal")))

    def increase_score(self):
        self.score += 1

    def update_score(self):
        self.undo()
        self.write(f"Score: {self.score}", False, "left", ("Verdana", 10, "normal"))
