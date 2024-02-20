from turtle import Turtle


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.color("white")
        self.hideturtle()
        self.penup()
        self.goto(-20, 350)
        self.right_score = 0
        self.left_score = 0

    def show_score(self):
        print(self.write(f"{self.left_score} {self.right_score}", False, "left", ("Verdana", 15, "normal")))

    def add_to_right_score(self):
        self.right_score += 1

    def add_to_left_score(self):
        self.left_score += 1

    def update_score(self):
        self.undo()
        self.show_score()
