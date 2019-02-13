import pygame
from tank import PlayerTank, Bullet, Wall, EnemyTank, Leaves, MainFlag
import sys
import os
import time

FPS = 50
WIDTH = 800
HEIGHT = 600

pygame.init()
pygame.key.set_repeat(200, 10)
STEP = 1
all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()
leaves = pygame.sprite.Group()
flags = pygame.sprite.Group()

clock = pygame.time.Clock()
height, width = 65  * 15, 65 * 16
screen = pygame.display.set_mode((width, height))

player_shot = False  # флаг-указатель наличия пули игрока на поле

screen_rect = (0, 0, width, height)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_width = tile_height = 65

# Flag = MainFlag(all_sprites, (100, 400), flags)
# leaves_wall = Wall(all_sprites, (100, 100), leaves, 'leaves')
# enemy = EnemyTank(all_sprites, enemies, (100, 300))
# wall = Wall(all_sprites, (400, 250), walls, 'brick')
# unbreak_wall = Wall(all_sprites, (300, 100), walls, 'steel')
# water_wall = Wall(all_sprites, (100, 200), walls, 'impassable')


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'W':
                Wall(all_sprites, (y * 65, x * 65), walls, 'impassable')
            elif level[y][x] == '#':
                Wall(all_sprites, (y * 65, x * 65), walls, 'steel')
            elif level[y][x] == 'F':
                MainFlag(all_sprites, (y * 65, x * 65), flags)
            elif level[y][x] == 'L':
                Wall(all_sprites, (y * 65, x * 65), leaves, 'leaves')
            elif level[y][x] == '*':
                Wall(all_sprites, (y * 65, x * 65), walls, 'brick')
            elif level[y][x] == 'E':
                EnemyTank(all_sprites, enemies, (y * 65, x * 65))
            elif level[y][x] == '@':
                new_player = PlayerTank(all_sprites, players, (y * 65, x * 65))
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


pygame.init()
running = True
start = False
player = None
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            # start = False
            if player is None:
                player, x, y = generate_level(load_level('test_level.txt'))
                print('aa')
            # if player[0] is not None:
            #     x = player[1]
            #     y = player[2]
            #     player = Player(x, y)
            all_sprites.add(player)
            players.add(player)
    all_sprites.draw(screen)
    players.draw(screen)
    leaves.draw(screen)
    pygame.display.flip()
    # if not start:
    # camera = Camera()
    # изменяем ракурс камеры
    # camera.update(player)
    # обновляем положение всех спрайтов
    # for sprite in all_sprites:
    #     camera.apply(sprite)
pygame.quit()
