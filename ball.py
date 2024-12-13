import pygame
import config
import math
import random


class Ball(pygame.sprite.Sprite):  # инициализируем клас Ball
    width = 20  # ширина мяча
    hight = 20  # высота мяча

    def __init__(self, game) -> None:  # определяем конструктор класса
        super().__init__()
        self.color = config.WHITE  # цвет мяча - белый
        self.speed = 10  # скорость мяча
        self.direction = 45  # направление в градусахь
        self.velocity_x = math.cos(math.radians(self.direction))  # x
        self.velocity_y = math.sin(math.radians(self.direction))  # y
        self.rect = pygame.Rect(0, 0, Ball.width, Ball.hight)  # создаём rect
        self.game = game  # передаём экземпляру game
        self.goto_start()  # вызываем метод goto_start
        self.sounds = {
            'collide': pygame.mixer.Sound(config.SOUND_DIR / 'ball.wav'),
            'goal': pygame.mixer.Sound(config.SOUND_DIR / 'goal.wav'),
        }

    def goto_start(self) -> None:  # определяем метод goto_start
        '''Переводит мяч на центр окна'''
        self.rect.centerx = self.game.window_widht * 0.5  # определяем ценр x
        self.rect.centery = self.game.window_height * 0.5  # определяем ценр y
        self.direction = random.randint(45, 135) * random.choice((-1, 1))

    def move(self) -> None:  # определяем метод move
        '''Двигает мяч'''
        self.velocity_x = math.cos(math.radians(self.direction - 90))
        self.velocity_y = math.sin(math.radians(self.direction - 90))
        self.rect.x += self.velocity_x * self.speed
        self.rect.y += self.velocity_y * self.speed

    def collide_barders(self) -> None:  # определяем метод collide_borders
        '''Не даёт мячу уйти за границы экрана'''
        if self.rect.top <= 0:
            self.direction *= -1
            self.direction += 180
            self.sounds['collide'].play()
        elif self.rect.bottom >= self.game.window_height:
            self.direction *= -1
            self.direction += 180
            self.sounds['collide'].play()

    def collide_rackets(self) -> None:  # определяем метод collide_rackets
        '''Не даёт мячу проходить сквозь ракетки'''
        if self.rect.colliderect(self.game.racket_left.rect):
            self.sounds['collide'].play()
            self.direction *= -1
        elif self.rect.colliderect(self.game.racket_right.rect):
            self.sounds['collide'].play()
            self.direction *= -1

    def score_goal(self) -> None:  # определяем метод score_goal
        '''Ведёт счёт забитых голов'''
        if self.rect.right >= self.game.window_widht:  # если гол справа
            self.sounds['goal'].play()
            self.game.goal_right += 1  # добовляем 1 к голам справа
            self.goto_start()  # вызываем метод goto_start

        elif self.rect.left <= 0:  # или если гол слева
            self.sounds['goal'].play()
            self.game.goal_left += 1  # добовляем 1 к голам слева
            self.goto_start()  # вызываем метод goto_start

    def render(self) -> None:  # определяем метод render
        '''Отрисовывоет rect мяча'''
        pygame.draw.rect(self.game.screen, self.color, self.rect, 0)  # рисуем

    def update(self) -> None:  # определяем метод update
        '''Обновляет состояния мяча'''
        self.collide_barders()  # вызываем метод collide_barders
        self.collide_rackets()  # вызываем метод collide_rackets
        self.move()  # вызываем метод move
        self.score_goal()  # вызываем метод score_goal
