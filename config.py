from pathlib import Path

RED = (255, 0, 0)  # красный
GREEN = (0, 255, 0)  # зелёный
BLUE = (0, 0, 255)  # синий
BLACK = (0, 0, 0)  # чёрный
WHITE = (255, 255, 255)  # белый
IS_DEBUG = False  # режим разработчика
FPS = 60  # кол-во отрисованных кадров в секунду

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / 'assets'
SOUND_DIR = ASSETS_DIR / 'sounds'
FONT_DIR = ASSETS_DIR / 'fonts'
