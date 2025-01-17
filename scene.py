import pygame
from abc import ABC, abstractmethod
import config
from ball import Ball  # импорт Ball из файла ball
from racket import RacketAuto, RacketManual
from score import Score  # импорт Score из файла score


class Scene(ABC):
    @abstractmethod
    def __init__(self, game):
        self.game = game
        self.keys_pressed = None
        self.all_sprites = pygame.sprite.Group()

    def handle_events(self) -> None:
        '''обрабатывает события'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.is_running = False

        self.keys_pressed = pygame.key.get_pressed()

    def update(self):
        self.all_sprites.update()

    def render(self):
        '''отрисовывает обьекты на екране'''
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()


class GameplayScene(Scene):
    def __init__(self, game, mode: str):
        super().__init__(game)
        self.all_rackets = pygame.sprite.Group()
        x_left = int(self.game.window_width * 0.1)
        x_right = int(self.game.window_width * 0.9)

        if mode in ('human_vs_pc', 'human_vs_human'):
            # левая ракетка
            self.racket_left = RacketManual(
                x_left,
                pygame.K_w,
                pygame.K_s,
                self
                )

        else:
            self.racket_left = RacketAuto(x_left, self)

        if mode in ('pc_vs_pc', 'human_vs_pc'):
            self.racket_right = RacketAuto(x_right, self)

        else:
            self.racket_right = RacketManual(
                x_right,
                pygame.K_UP,
                pygame.K_DOWN,
                self)

        # мяч
        self.ball = Ball(self)

        # левое табло
        self.score_left = Score(int(self.game.window_width * 0.25), 100, self)

        # правое табло
        self.score_right = Score(int(self.game.window_width * 0.75), 100, self)

    def render(self):
        '''отрисовывает обьекты на екране'''
        self.game.screen.fill(config.BLACK)
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()


class MenuScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        MenuLines(
            self,
            '1 - человек vs компьютер',
            '2 - человек vs человек',
            '3 - компьютер vs компьютер',
            'esc - выход',
        )

    def handle_events(self):
        super().handle_events()
        if self.keys_pressed[pygame.K_1]:
            self.game.scene = GameplayScene(self.game, 'human_vs_pc')
        elif self.keys_pressed[pygame.K_2]:
            self.game.scene = GameplayScene(self.game, 'human_vs_human')
        elif self.keys_pressed[pygame.K_3]:
            self.game.scene = GameplayScene(self.game, 'pc_vs_pc')

    def render(self):
        self.game.screen.fill(config.BLACK)
        self.all_sprites.draw(self.game.screen)
        pygame.display.flip()


class Text(pygame.sprite.Sprite):
    def __init__(self, text_line: str, cords: tuple):
        super().__init__()
        font = pygame.font.Font(None, 74)
        self.image = font.render(text_line, True, config.WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = cords


class MenuLines:
    def __init__(self, scene, *lines):
        x = scene.game.window_width // 2
        y = 100
        for line in lines:
            text_line = Text(line, (x, y))
            scene.all_sprites.add(text_line)
            y += 100
