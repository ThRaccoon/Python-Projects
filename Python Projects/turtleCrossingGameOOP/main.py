import turtle
from turtle import Screen, Turtle
from player import Player
from car import Car
from score import Score
import time
import random


def objects_scale(_object_weight, _object_height, _new_screen_weight, _new_screen_height, _default_screen_weight, _default_screen_height):
    func_screen_weight_scale = _new_screen_weight / _default_screen_weight
    func_screen_height_scale = _new_screen_height / _default_screen_height

    func_object_weight = round(_object_weight * func_screen_weight_scale, 2)
    func_object_height = round(_object_height * func_screen_height_scale, 2)

    return func_object_weight, func_object_height


def collider_scale(_default_collider, _default_screen_height, _new_screen_height):
    func_collider = (_new_screen_height / _default_screen_height) * _default_collider
    return round(func_collider, 2)


def offset_scale(_default_offset, _default_screen_height, _new_screen_height):
    original_offset = (_default_screen_height / 8) + _default_offset
    func_offset = (_new_screen_height / _default_screen_height) * original_offset
    return round(func_offset, 2)


def cal_offset(_offset, screen_weight, screen_height):
    b = _offset
    list2 = [b]
    for j in range(3):
        b += _offset
        if j < 3:
            list2.append(b)
        if j == 2:
            player_x_pos = screen_weight / screen_weight
            player_y_pos = screen_height / 2 - (b + _offset)
            list2.append(player_x_pos)
            list2.append(player_y_pos)

    return list2


def spawn_cars():
    func_list_of_cars = []
    list_of_positions = (list_of_pos[0], list_of_pos[1], list_of_pos[2], list_of_pos[3])
    # position = random.choice(list_of_positions)
    # car = Car(new_car_weight, new_car_height, new_screen_weight, new_screen_height, position)
    # return car

    num1 = random.randint(1, 9)
    if num1 == 1:
        car = Car(new_car_weight, new_car_height, new_screen_weight, new_screen_height, list_of_pos[0])
        func_list_of_cars.append(car)
    num2 = random.randint(1, 9)
    if num2 == 5:
        car = Car(new_car_weight, new_car_height, new_screen_weight, new_screen_height, list_of_pos[1])
        func_list_of_cars.append(car)
    num3 = random.randint(1, 12)
    if num3 == 3:
        car = Car(new_car_weight, new_car_height, new_screen_weight, new_screen_height, list_of_pos[2])
        func_list_of_cars.append(car)
    num4 = random.randint(1, 12)
    if num4 == 8:
        car = Car(new_car_weight, new_car_height, new_screen_weight, new_screen_height, list_of_pos[3])
        func_list_of_cars.append(car)
    return func_list_of_cars


player_weight = 1.6
player_height = 1.4
car_weight = 1.8
car_height = 2.2
DEFAULT_SCREEN_WEIGHT = 600  # Do not change
DEFAULT_SCREEN_HEIGHT = 600  # Do not change
new_screen_weight = 400  # Change but keep aspect ratio 1:1 or 4:3
new_screen_height = 400  # Change but keep aspect ratio 1:1 or 4:3
DEFAULT_COLLIDER = 33
DEFAULT_OFFSET = 18

new_player_weight, new_player_height = objects_scale(player_weight, player_height, new_screen_weight, new_screen_height,
                                                     DEFAULT_SCREEN_WEIGHT, DEFAULT_SCREEN_HEIGHT)

new_car_weight, new_car_height = objects_scale(car_weight, car_height, new_screen_weight, new_screen_height,
                                               DEFAULT_SCREEN_WEIGHT, DEFAULT_SCREEN_HEIGHT)

collider = collider_scale(DEFAULT_COLLIDER, DEFAULT_SCREEN_HEIGHT, new_screen_height)
offset = offset_scale(DEFAULT_OFFSET, DEFAULT_SCREEN_HEIGHT, new_screen_height)

screen = Screen()
screen.setup(new_screen_weight, new_screen_height)
screen.title("Turtle crossing")
screen.bgcolor("honeydew2")
screen.tracer(0)

game_score = Score(-50, new_screen_height / 2 - 50)
game_score.show_score()
final_score = Score((new_screen_weight / 4) * -1, 0)

list_of_pos = cal_offset(offset, new_screen_weight, new_screen_height)

player = Player(offset, new_player_weight, new_player_height, list_of_pos[4], list_of_pos[5])

screen.listen()
screen.onkey(player.move, "space")
screen.onkey(player.move_up, "w")
# screen.onkey(player.move_down, "s")
screen.onkey(player.move_left, "d")
screen.onkey(player.move_right, "a")


list_of_cars = []
list_of_cars += spawn_cars()

counter = 0

game_on = True
while game_on:

    list_of_cars += spawn_cars()
    print(len(list_of_cars))

    if player.player.ycor() >= new_screen_height - (new_screen_height / 2) - 10:
        counter += 1
        game_score.add_to_score()
        if counter == 3:
            for k in range(len(list_of_cars) - 1, -1, -1):
                list_of_cars[k].car.hideturtle()
            game_score.update_score()
            player.player.hideturtle()
            final_score.write("You crossed successfully!", False, "left", ("Verdana", 15, "normal"))
            game_on = False
        else:
            game_score.update_score()
            player.player.teleport(list_of_pos[4], list_of_pos[5])
            for k in range(len(list_of_cars) - 1, -1, -1):
                list_of_cars[k].car.hideturtle()
                list_of_cars.pop(k)

    for i in range(len(list_of_cars)):
        if player.player.distance(list_of_cars[i].car_x_cor(), list_of_cars[i].car_y_cor()) <= collider:
            final_score.write("You got smashed by a car!", False, "left", ("Verdana", 15, "normal"))
            player.player.hideturtle()
            for k in range(len(list_of_cars) - 1, -1, -1):
                list_of_cars[k].car.hideturtle()
                game_on = False

    for j in range(len(list_of_cars)):
        list_of_cars[j].car_move()

    for k in range(len(list_of_cars) -1, -1, -1):
        if list_of_cars[k].car.xcor() <= -310:
            list_of_cars[k].car.hideturtle()
            list_of_cars.pop(k)

    screen.update()
    time.sleep(0.1)

screen.exitonclick()
