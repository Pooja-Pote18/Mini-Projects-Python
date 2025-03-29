import turtle
import random
import time

delay = 0.1
sc = 0
hs = 0
bodies = []

# creating a screen
s = turtle.Screen()
s.title("Snake Game")
s.bgcolor("lightblue")
s.setup(width=500, height=500)  # size of the screen

# creating the snake head
head = turtle.Turtle()
head.speed(0)
head.shape("circle")
head.color("black")
head.fillcolor("red")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# creating food
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("white")
food.fillcolor("blue")
food.penup()
food.ht()
food.goto(150, 250)
food.st()
food.direction = "stop"

# scoreboard
sb = turtle.Turtle()
sb.ht()
sb.penup()
sb.goto(-250, 250)
sb.write("score:0 | Highest score:0")  # to print msg on screen

# position
def move_up():
    if head.direction != "down":
        head.direction = "up"

def move_down():
    if head.direction != "up":
        head.direction = "down"

def move_left():
    if head.direction != "right":
        head.direction = "left"

def move_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)


# Event handling - key mapping
s.listen()
s.onkey(move_up, "Up")
s.onkey(move_down, "Down")
s.onkey(move_left, "Left")
s.onkey(move_right, "Right")

# main loop
while True:
    s.update()  # to update screen

    # check collision with border    
    if head.xcor() > 290:
        head.setx(-290)
    if head.xcor() < -290:
        head.setx(290)
    if head.ycor() > 290:
        head.sety(-290)
    if head.ycor() < -290:
        head.sety(290)

    # check collision with food
    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)
        # increase length of snake
        body = turtle.Turtle()
        body.speed(0)
        body.penup()
        body.shape("square")
        body.color("green")
        bodies.append(body)

        # increase score
        sc += 10
        if sc > hs:
            hs = sc
        sb.clear()
        sb.write("score:{} | Highest score:{}".format(sc, hs))
        # increase speed
        delay -= 0.001

    # move snake bodies
    for index in range(len(bodies) - 1, 0, -1):
        x = bodies[index - 1].xcor()
        y = bodies[index - 1].ycor()
        bodies[index].goto(x, y)

    if len(bodies) > 0:
        x = head.xcor()
        y = head.ycor()
        bodies[0].goto(x, y)

    move()

    # check collision with snake body
    for body in bodies:
        if body.distance(head) < 20:
            time.sleep(1)  # Fixed typo here
            head.goto(0, 0)
            head.direction = "stop"
            for body in bodies:
                body.ht()  # Hide all body segments
            bodies.clear()
            sc = 0
            delay = 0.1
            sb.clear()
            sb.write("score:{} | Highest score:{}".format(sc, hs))

    time.sleep(delay)