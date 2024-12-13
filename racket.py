import pygame
import config


class Racket(pygame.sprite.Sprite):  # инициализируем класс Racket
    def __init__(
            self,
            center_x: int,
            game,
    ) -> None:  # конструктор
        super().__init__()
        self.game = game  # передаём класс game
        self.center_x = center_x  # задаём x центра ракетки
        sreen_width, screen_hight = self.game.screen.get_size()
        self.speed = Racket.speed  # определяем скорость ракетки
        self.rect = pygame.Rect(0, 0, Racket.width, Racket.hight)  # rect
        self.color = config.WHITE  # цвет - белый
        self.goto_start()  # вызываем метод goto_start
        self.delay = 10  # задержка бота
        self.last_move = pygame.time.get_ticks()  # таймер ракетки
        self.game.all_sprites.add(self)

    def goto_start(self):  # определяем метод goto_start
        '''Переносит ракетку на стартовую позицию'''
        self.rect.centerx = self.center_x  # x центра
        self.rect.centery = self.game.window_height * 0.5  # y центра

    def move(self):
        '''двигает ракетку'''
        pass

    def collide_borders(self) -> None:  # определяем метод collide_borders
        '''Не даёт ракеткам уходить в стены'''
        if self.rect.bottom > self.game.window_height:  # если ракетка внизу
            self.rect.bottom = self.game.window_height  # переносим её дно
        elif self.rect.top < 0:  # если ракетка вверху
            self.rect.top = 0  # переносим её верх

    def render(self) -> None:  # определяем метод render
        '''Отрисовывает rect ракетки'''
        pygame.draw.rect(  # отрисовываем rect ракетки
                        self.game.screen,  # мастер
                        self.color,  # цвет
                        self.rect,  # rect
                        self.width  # ширина
                        )
        pygame.display.flip()  # 'переворачиваем' экран

    def update(self) -> None:  # определяем метод update
        '''Обновляет состояния ракетки'''
        self.collide_borders()  # вызываем метод collide_borders
        self.move()


class RacketAuto(Racket):
    def __init__(
            self,
            center_x: int,
            game,
            ) -> None:
        super().__init__(
            center_x,
            game,
            )

    def move(self) -> None:  # определение метода move
        if pygame.time.get_ticks() - self.last_move >= self.delay:
            if self.game.ball.rect.centery < self.rect.y:
                self.rect.y -= self.speed
            elif self.game.ball.rect.centery > self.rect.y:
                self.rect.y += self.speed
            self.last_move = pygame.time.get_ticks()


class RacketManual(Racket):
    def __init__(
            self,
            center_x: int,
            game,
            ) -> None:
        self.key_down = pygame.K_s
        self.key_up = pygame.K_w
        super().__init__(center_x, game)

    def move(self):
        if self.game.keys_pressed[self.key_down]:  # если клавиша вниз
            self.rect.y += self.speed  # y ракетки больше на скорость
        elif self.game.keys_pressed[self.key_up]:  # если клавиша вверх
            self.rect.y -= self.speed  # y ракетки меньше на скорость
