from turtle import Screen
from paddle import Paddle
from ball import Ball
from score import Score
from border import Border
import time

screen = Screen()
screen.setup(950, 750)
screen.bgcolor("black")
screen.title("Pong")
screen.tracer(0)

border = Border()
border.draw_border()

rPaddle = Paddle(400, 0)
lPaddle = Paddle(-400, 0)

score = Score()
score.show_score()

ball = Ball()

screen.listen()
screen.onkey(rPaddle.move_up, "o")
screen.onkey(rPaddle.move_down, "l")
screen.onkey(lPaddle.move_up, "w")
screen.onkey(lPaddle.move_down, "s")


random_direction = True
game_on = True
while game_on:

    if random_direction:
        ball.start_move()

    if not random_direction:
        ball.move()

    if (ball.xcor() >= 350 and ball.distance(rPaddle) <= 60) or \
       (ball.xcor() <= -350 and ball.distance(lPaddle) <= 60):
        ball.bounce_x()
        random_direction = False

    if ball.ycor() > 320 or ball.ycor() < -330:
        ball.bounce_y()
        random_direction = False

    if ball.xcor() < -455:
        score.add_to_right_score()
        score.update_score()
        random_direction = True
        ball.reset_ball()

    if ball.xcor() > 450:
        score.add_to_left_score()
        score.update_score()
        random_direction = True
        ball.reset_ball()

    if score.left_score >= 3 or score.right_score >= 3:
        if score.left_score >= 3:
            print(f"GAME OVER LEFT SIDE WON!")
        else:
            print(f"GAME OVER RIGHT SIDE WON!")
        game_on = False
        screen.exitonclick()

    screen.update()
    time.sleep(0.1)
