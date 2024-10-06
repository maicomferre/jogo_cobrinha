import turtle
import random
import time
from random import randint
from tkinter import *
import pygame
import glob

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
BORDER_COLOR = 'red'
BORDER_PENSIZE = 4
BORDER_SPEED = 5
FOOD_SHAPE = 'square'
FOOD_COLOR_NEW = 'red'
FOOD_COLOR_OLD = 'white'
SNAKE_SHAPE = 'square'
SNAKE_COLOR = 'green'
INITIAL_DELAY = 0.1
SCORE_FONT = ("Courier", 24, "bold")
GAME_OVER_FONT = ("Courier", 30, "bold")

class Game:
    def __init__(self):
        self.get_nick_name = None
        self.nickname = ""
        self.btn_button = None
        self.btn_label = None
        pygame.mixer.init()
        self.food_sound = []
        self.kill_sound = []

        pygame.mixer.init()
        for x in glob.glob('sound_effects/foods/*.mp3'):
            self.food_sound.append(pygame.mixer.Sound(x))
        self.food_sound_size = len(self.food_sound)-1

        for x in glob.glob('sound_effects/kill/*.mp3'):
            self.kill_sound.append(pygame.mixer.Sound(x))
        self.kill_sound_size = len(self.kill_sound)-1

        self.screen = self.setup_screen()
        self.snake = self.create_snake()
        self.panel = self.setup_game_panel()
        self.fruit = self.create_food()
        self.old_fruits = []
        self.score = 0
        self.delay = INITIAL_DELAY
        self.draw_border()
        self.bind_keys()

        canva = self.screen.getcanvas().master

        self.btn_label = Label(canva, text="Digite seu nickname: ",
                width=25, height=10, bg="lightblue", bd=5, relief=RIDGE, font=("FreeSans", 24, "bold"))
        self.btn_label.pack()
        self.btn_label.place(x=110, y=175)

        self.get_nick_name = Entry(canva,font=("FreeSans", 24, "bold"))
        self.get_nick_name.pack()
        self.get_nick_name.place(x=155, y=370)

        self.btn_button = Button(canva, text="Iniciar Jogo", command=self.set_nickname,font=("FreeSans", 24, "bold"))
        self.btn_button.pack()
        self.btn_button.place(x=230, y=420)
        self.screen.listen()
        self.screen.onkeypress(self.set_nickname, "Return")

        canva.mainloop()

    def setup_screen(self):
        screen = turtle.Screen()
        screen.title("Jogo da Cobrinha")
        screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        screen.tracer(0)
        screen.bgpic('PIXNIO-1050210-544x544.png')

        return screen

    def draw_border(self):
        turtle.speed(BORDER_SPEED)
        turtle.pensize(BORDER_PENSIZE)
        turtle.penup()
        turtle.goto(-310, 250)
        turtle.pendown()
        turtle.color(BORDER_COLOR)
        for _ in range(2):
            turtle.forward(600)
            turtle.right(90)
            turtle.forward(500)
            turtle.right(90)
        turtle.penup()
        turtle.hideturtle()

    def setup_game_panel(self):
        panel = turtle.Turtle()
        panel.speed(0)
        panel.color('white')
        panel.penup()
        panel.hideturtle()
        panel.goto(0, 260)
        panel.write("PlayerName: ", align="center", font=SCORE_FONT)

        scoring = turtle.Turtle()
        scoring.speed(0)
        scoring.color("black")
        scoring.penup()
        scoring.hideturtle()
        scoring.goto(0, 300)
        scoring.write("Score: 0", align="center", font=SCORE_FONT)

        self.scoring = scoring
        return panel

    def create_snake(self):
        snake = turtle.Turtle()
        snake.speed(0)
        snake.shape(SNAKE_SHAPE)
        snake.color(SNAKE_COLOR)
        snake.penup()
        snake.goto(0, 0)
        snake.direction = "stop"
        return snake

    def create_food(self):
        food = turtle.Turtle()
        food.speed(0)
        food.shape(FOOD_SHAPE)
        food.color(FOOD_COLOR_OLD)
        food.penup()
        food.goto(30, 30)
        return food

    def bind_keys(self):
        self.screen.listen()
        self.screen.onkeypress(self.move_up, "Up")
        self.screen.onkeypress(self.move_down, "Down")
        self.screen.onkeypress(self.move_left, "Left")
        self.screen.onkeypress(self.move_right, "Right")

    def move_up(self):
        if self.snake.direction != "down":
            self.snake.direction = "up"

    def move_down(self):
        if self.snake.direction != "up":
            self.snake.direction = "down"

    def move_left(self):
        if self.snake.direction != "right":
            self.snake.direction = "left"

    def move_right(self):
        if self.snake.direction != "left":
            self.snake.direction = "right"

    def move_snake(self):
        if self.snake.direction == "up":
            self.snake.sety(self.snake.ycor() + 20)
        if self.snake.direction == "down":
            self.snake.sety(self.snake.ycor() - 20)
        if self.snake.direction == "left":
            self.snake.setx(self.snake.xcor() - 20)
        if self.snake.direction == "right":
            self.snake.setx(self.snake.xcor() + 20)

    def play_sound(self, sound):
        if sound == 'eat':
            self.food_sound[randint(0, self.food_sound_size)].play()
        if sound == 'kill':
            self.kill_sound[randint(0, self.kill_sound_size)].play()

    def start_game(self):
        self.bind_keys()
        while True:
            self.screen.update()
            if self.snake.distance(self.fruit) < 15:
                self.play_sound('eat')
                self.fruit.goto(random.randint(-290, 270), random.randint(-240, 240))
                self.score += 1
                self.delay -= 0.0007
                self.update_score()

                new_fruit = turtle.Turtle()
                new_fruit.speed(0)
                new_fruit.shape(FOOD_SHAPE)
                new_fruit.color(FOOD_COLOR_NEW)
                new_fruit.penup()
                self.old_fruits.append(new_fruit)

            self.move_old_fruits()
            self.move_snake()
            self.check_collisions()
            time.sleep(self.delay)

    def update_score(self):
        self.scoring.clear()
        self.scoring.write(f"Score: {self.score}", align="center", font=SCORE_FONT)

    def move_old_fruits(self):
        for index in range(len(self.old_fruits) - 1, 0, -1):
            x = self.old_fruits[index - 1].xcor()
            y = self.old_fruits[index - 1].ycor()
            self.old_fruits[index].goto(x, y)

        if self.old_fruits:
            self.old_fruits[0].goto(self.snake.xcor(), self.snake.ycor())

    def check_collisions(self):
        if (self.snake.xcor() > 280 or self.snake.xcor() < -300 or
            self.snake.ycor() > 240 or self.snake.ycor() < -240):
            self.game_over()

        for fruit in self.old_fruits:
            if fruit.distance(self.snake) < 20:
                self.game_over()

    def game_over(self):
        self.play_sound('kill')
        time.sleep(1)
        self.screen.clear()
        self.screen.bgcolor('turquoise')
        self.scoring.goto(0, 0)
        self.scoring.write(f"  GAME OVER\nSeu Score é {self.score}", align="center", font=GAME_OVER_FONT)
        time.sleep(3)

        # Não fechar a janela, apenas reiniciar
        self.screen.clearscreen()
        self.__init__()  # Reiniciar o jogo

    def set_nickname(self):
        self.panel.clear()
        self.nickname = self.get_nick_name.get()
        if len(self.nickname) == 0:
            self.nickname = random.choice(("John", "Andy","Joe", "James", "Noah"))
        self.panel.write("PlayerName: " +  self.nickname , align="center", font=SCORE_FONT)
        self.btn_label.destroy()
        self.btn_button.destroy()
        self.get_nick_name.destroy()
        # Iniciar o jogo após o nickname ser definido
        self.start_game()

if __name__ == '__main__':
    game = Game()
