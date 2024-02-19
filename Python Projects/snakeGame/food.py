from turtle import Turtle


class Food(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_list = []
        self.spawn_food()

    def spawn_food(self):
        food = Turtle(shape="circle")
        food.penup()
        food.color("blue")
        food.shapesize(0.8)
        self.food_list.append(food)
        self.food_list[0].goto(self.x, self.y)

    def del_food(self):
        self.food_list[0].ht()
        self.food_list.pop(0)


