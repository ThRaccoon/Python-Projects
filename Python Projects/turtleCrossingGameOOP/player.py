from turtle import Turtle


class Player(Turtle):
    def __init__(self, offset, new_player_weight, new_player_height, player_x_pos, player_y_pos):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.goto(-400, -400)
        self.player = Turtle()
        self.player.penup()
        self.player.shape("turtle")
        self.player.color("green")
        self.player.shapesize(new_player_weight, new_player_height)
        self.player.teleport(player_x_pos, player_y_pos)
        self.player.left(90)
        self.offset = offset

    def x(self):
        return self.player.xcor()

    def y(self):
        return self.player.ycor()

    def player_boundaries(self, player_x, player_y):
        if self.player.xcor() < -150:
            self.player.goto(player_x + (self.offset / 2 - 1), player_y)
        if self.player.xcor() > 150:
            self.player.goto(player_x - (self.offset / 2 - 1), player_y)

    def move(self):
        self.player.forward(self.offset / 2 - 1)

    def move_up(self):
        self.player.setheading(90)

    def move_down(self):
        self.player.setheading(270)

    def move_right(self):
        self.player.setheading(180)

    def move_left(self):
        self.player.setheading(0)

