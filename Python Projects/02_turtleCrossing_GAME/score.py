from turtle import Turtle


class Score(Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.color("black")
        self.hideturtle()
        self.penup()
        self.goto(x, y)
        self.score = 0
        self.record = 0

    def show_score(self):
        print(self.write(f"Score: {self.score}| Record: {self.record}", False, "left", ("Verdana", 15, "normal")))

    def add_to_score(self):
        self.score += 1

    def update_score(self):
        self.undo()
        self.show_score()

    def update_record(self):
        if self.score > self.record:
            self.record = self.score

