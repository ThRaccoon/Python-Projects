from turtle import Turtle


class Snake(object):
    def __init__(self):
        self.snake_list = []
        self.create_snake()
        self.head = self.snake_list[0]

    def create_snake(self):
        x = 0
        for i in range(3):
            new_snake = Turtle(shape="square")
            new_snake.color("white")
            new_snake.speed("slowest")
            new_snake.shapesize(0.8)
            new_snake.penup()
            new_snake.setpos(x, 0)
            x -= 20
            self.snake_list.append(new_snake)

    def move_forwards(self):
        for i in range(len(self.snake_list) - 1, 0, - 1):
            self.snake_list[i].goto(self.snake_list[i - 1].xcor(), self.snake_list[i - 1].ycor())
        self.head.forward(20)

    def eat(self):
        new_snake = Turtle(shape="square")
        new_snake.color("white")
        new_snake.speed("slowest")
        new_snake.shapesize(0.8)
        new_snake.penup()
        new_snake.setpos(-320, -320)
        self.snake_list.append(new_snake)

    def turn_up(self):
        if self.head.heading() != 270:
            self.head.setheading(90)

    def turn_down(self):
        if self.head.heading() != 90:
            self.head.setheading(270)

    def turn_right(self):
        if self.head.heading() != 180:
            self.head.setheading(0)

    def turn_left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)

    def head_x_cords(self):
        return round(self.head.xcor())

    def head_y_cords(self):
        return round(self.head.ycor())

    def snake_x_cords(self):
        list_x = []
        for i in range(len(self.snake_list)):
            list_x.append(round(self.snake_list[i].xcor()))
        return list_x

    def snake_y_cords(self):
        list_y = []
        for i in range(len(self.snake_list)):
            list_y.append(round(self.snake_list[i].ycor()))
        return list_y
