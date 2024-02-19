from turtle import Turtle, Screen
from snake import Snake
from food import Food
from score import Score
from border import Border
import random
import time

screen = Screen()
screen.setup(480, 480)
screen.bgcolor("black")
screen.title("Snake")
screen.tracer(0)

score = Score()
text_score = Turtle()
border = Border()
snake = Snake()

screen.listen()
screen.onkey(snake.turn_up, "w")
screen.onkey(snake.turn_down, "s")
screen.onkey(snake.turn_right, "d")
screen.onkey(snake.turn_left, "a")


def spawn_food():
    x_cords = (-140, -120, -100, -80, -60, -40, -20, 20, 40, 60, 80, 100, 120, 140)
    y_cords = (-140, -120, -100, -80, -60, -40, -20, 20, 40, 60, 80, 100, 120, 140)
    snake_x = snake.snake_x_cords()
    snake_y = snake.snake_y_cords()
    list1 = []
    for i in range(len(snake_x)):
        list1.append((snake_x[i], snake_y[i]))

    list2 = []
    food_x = random.choice(x_cords)
    food_y = random.choice(y_cords)
    list2.append((food_x, food_y))
    check = any(item in list2 for item in list1)
    if check is True:
        print(f"Old x:{food_x} | Old y: {food_y}")
        while check is True:
            food_x = random.choice(x_cords)
            food_y = random.choice(y_cords)
            list2.clear()
            list2.append((food_x, food_y))
            check = any(item in list2 for item in list1)
        print(f"New x:{food_x} | New y: {food_y}")
        return food_x, food_y
    else:
        return food_x, food_y


def check_if_head_collides_with_body():
    snake_x = snake.snake_x_cords()
    snake_y = snake.snake_y_cords()
    for i in range(1, len(snake_x)):
        if snake.head_x_cords() == snake_x[i] and snake.head_y_cords() == snake_y[i]:
            print("Death: You collided with your body!")
            exit(print(f"Your score is {score.score}"))


def check_if_head_collides_with_walls():
    snake_x = snake.head_x_cords()
    snake_y = snake.head_y_cords()
    if (snake_x <= -180 or snake_x >= 180) or (snake_y <= -180 or snake_y >= 180):
        print("Death: You collided with a wall!")
        exit(print(f"Your score is {score.score}"))


border.draw_border()
score.draw_score()
food_x_cords, food_y_cords = spawn_food()
food = Food(food_x_cords, food_y_cords)

while True:
    check_if_head_collides_with_walls()
    check_if_head_collides_with_body()

    if food_x_cords == snake.head_x_cords() and food_y_cords == snake.head_y_cords():
        score.increase_score()
        score.update_score()
        food.del_food()
        del food
        snake.eat()
        food_x_cords, food_y_cords = spawn_food()
        food = Food(food_x_cords, food_y_cords)
    screen.update()
    time.sleep(0.1)
    snake.move_forwards()
