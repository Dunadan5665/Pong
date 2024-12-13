'''
||||||     ||||    ||||   ||   ||||||
||   ||  ||    ||  || ||  ||  ||
||||||   ||    ||  ||  || ||  ||  |||
||         ||||    ||   ||||   |||||
'''

import pygame
import config
from ball import Ball
from racket import Racket, RacketAuto, RacketManual


class Game:  # инициализация класса Game
    def __init__(self) -> None:  # определение конструктора класса
        pygame.init()  # определение pygame
        pygame.mixer.init()
        display_info = pygame.display.Info()  # инфо об окне
        self.window_widht = display_info.current_w  # ширина окна
        self.window_height = display_info.current_h  # высота окна
        self.goal_left = 0  # кол-во голов слева
        self.goal_right = 0  # кол-во голов справа
        self.ball = Ball(self)
        self.is_auto = True  # игра с ботом

        self.all_sprites = pygame.sprite.Group()

        x_left = int(self.window_widht * 0.1)  # x левой ракетки
        self.racket_left = RacketManual(center_x=x_left, game=self)

        x_right = int(self.window_widht * 0.9) - Racket.width  # x правой
        self.racket_right = RacketAuto(x_right, self)  # создаём ракетку авто

        self.screen = pygame.display.set_mode(  # определяем окно игры
            (self.window_widht, self.window_height)  # задаём размеры
        )

        self.is_running = True  # индикатор зажатия клавиши
        self.clock = pygame.time.Clock()  # экземпляр часов

    def show_run(self) -> None:
        pass

    def main_loop(self) -> None:  # определяем основной цикл игры
        '''
        сбор событий
        обновление (объектов)
        рендер
        ожидание FPS
        '''
        while self.is_running:  # пока клавиша зажата
            self.handle_events()  # вызов handle_events
            self.update()  # вызов update
            self.render()  # вызов render
            self.clock.tick(config.FPS)  # кол-во отрисованных кадров в секунду
        pygame.quit()  # закрываем окно

    def update(self) -> None:  # определяем метод update
        '''Обновляет состояния игры'''
        self.ball.update()  # вызов метода update от Ball
        self.racket_right.update()  # вызов метода update от левой ракетки
        self.racket_left.update()  # вызов метода update от правой ракетки

    def handle_events(self) -> None:
        '''обрабатывает события'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
        self.keys_pressed = pygame.key.get_pressed()

    def render(self) -> None:  # определение метода render
        '''Отрисовка спрайтов'''
        self.screen.fill(config.BLACK)  # заливка эрана - BLACK
        if config.IS_DEBUG:  # если включен режим разработчика
            pygame.draw.line(  # отрисовываем правую линию
                self.screen,  # мастер объекта
                config.GREEN,  # цвет - зелёный
                (int(self.window_widht * 0.1), 0),  # нач. координата
                (int(self.window_widht * 0.1), self.window_height)  # кон.коорд
                )

            pygame.draw.line(  # отрисовываем левую линию
                self.screen,  # мастер объекта
                config.BLUE,  # цвет - синий
                (int(self.window_widht * 0.9), 0),  # нач. координата
                (int(self.window_widht * 0.9), self.window_height)  # кон.коорд
                )

            pygame.draw.line(  # отрисовываем центральную горизонтальную линию
                self.screen,  # мастер объекта
                config.RED,  # цвет - красный
                (0, self.window_height // 2),  # нач. координата
                (self.window_widht, self.window_height // 2)  # кон.коорд
                )

        pygame.draw.line(  # отрисовка центральной, игровой линии
            self.screen,  # мастер объекта
            config.WHITE,  # цвет - белый
            (self.window_widht // 2, 0),  # нач. координата
            (self.window_widht // 2, self.window_height)  # кон.коорд
            )
        self.racket_left.render()  # вызов метода render от левой ракетки
        self.racket_right.render()  # вызов метода render от правой ракетки
        self.ball.render()  # вызов метода render от мяча
        self.create_counters()  # вызов метода create_counters
        pygame.display.flip()  # 'переварачиваем' экран

    def create_counters(self) -> None:  # определяем метод create_counters
        '''Создаёт счётчики забитых голов'''
        font = pygame.font.Font(config.FONT_DIR / 'thin_pixel-7.ttf', 150)
        score_left_text = font.render(
            str(self.goal_left),
            True,
            config.WHITE
            )  # рендерим левый счётчик
        score_right_text = font.render(
            str(self.goal_right),
            True,
            config.WHITE
            )  # рендерим правый счётчик
        self.screen.blit(
            score_left_text,
            (self.window_widht // 4, 100)
            )  # отрисовываем левый счётчик на окне
        self.screen.blit(
            score_right_text,
            (3*self.window_widht // 4, 100)
            )  # отрисовываем правый счётчик на окне


if __name__ == '__main__':  # если запуск из этого файла
    Game().main_loop()  # создаём экземпляр класса Game
