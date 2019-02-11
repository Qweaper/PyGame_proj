import pygame
from tank import PlayerTank, Bullet, Wall, EnemyTank, Leaves, MainFlag
import sys
import os
import random
import time

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()
leaves = pygame.sprite.Group()
flags = pygame.sprite.Group()
clock = pygame.time.Clock()
FPS = 50


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


# Класс танка игрока

class PlayerTank(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('tank.png'), (65, 65))

    def __init__(self, def_group, group, startpos=(500, 500)):
        super().__init__(def_group)
        # self.x = None
        # self.y = None
        self.impassible = {
            'up': True,
            'down': True,
            'left': True,
            'right': True
        }
        # загрузка картинки
        self.image = PlayerTank.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Переменная отвечающая за напрваление движения
        # И положение картинки
        self.direction = 'up'
        self.images = {
            'up': self.image,
            'down': pygame.transform.scale(pygame.transform.rotate(self.image, 180), (65, 65)),
            'right': pygame.transform.scale(pygame.transform.rotate(self.image, 270), (65, 65)),
            'left': pygame.transform.scale(pygame.transform.rotate(self.image, 90), (65, 65))
        }

        # пока не будет музыки передвижения
        # добавим ближе к завершению
        self.sound = None

        # создание маски
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = startpos[0]
        self.rect.y = startpos[1]
        # переменные для жизней и кол-ва ранений
        self.wounds = 1  # ранения
        self.lifes = 3  # жизни
        group.add(self)

        #
        # надо добавить метод спавна танка на позиции
        #
        self.res_pos = startpos

    # метод взрыва
    def explose(self):
        self.wounds -= 1
        if self.wounds == 0:
            self.image = pygame.transform.scale(load_image('explosion.png'), (65, 65))
            #
            # Добавить анимацию взрыва
            #
            self.lifes -= 1
            clock.tick(FPS)
            self.kill()

            if self.lifes != 0:
                self.spawn()

    # метод респавна танка
    def spawn(self):
        self.image = self.images[self.direction]
        self.rect.x, self.rect.y = self.res_pos
        self.wounds = 1

    # метод для возпращения позиции(пока не используется)
    def pos(self):
        return self.rect.x, self.rect.y, self.rect.width, self.rect.height

    # движение танка игрока
    def move(self, direct):
        next_pos = direct[-1]
        direct = direct[0]
        # self.mask = self.mask = pygame.mask.from_surface(self.images[next_pos])
        # self.image = self.images[next_pos]
        other = pygame.sprite.spritecollide(self, walls, False)
        self.impassible['up'] = True
        self.impassible['down'] = True
        self.impassible['left'] = True
        self.impassible['right'] = True
        if len(other) != 0:
            for i in pygame.sprite.spritecollide(self, walls, False):
                # print(self.rect.x in range(i.pos()[0] - i.rect.width, i.pos()[0] + i.rect.width))
                # print(self.rect.y in range(i.pos()[1] - i.rect.height, i.pos()[1] + i.rect.height))
                # if i.pos()[0] == self.rect.x and self.rect.y < i.pos()[1]:
                if self.rect.y in range(i.pos()[1] - i.rect.height, i.pos()[1] + 1):
                    self.impassible['down'] = False
                    print(1)
                    # continue
                # if i.pos()[0] == self.rect.x and i.pos()[1] < self.rect.y:
                if self.rect.y in range(i.pos()[1], i.pos()[1] + height + 1):
                    self.impassible['up'] = False
                    print(2)
                    # continue
                # if i.pos()[0] > self.rect.x and i.pos()[1] == self.rect.y:
                if self.rect.x in range(i.pos()[0], i.pos()[0] + i.rect.width + 1):
                    self.impassible['left'] = False
                    print(3)
                    # continue
                # if i.pos()[0] < self.rect.x and i.pos()[1] == self.rect.y:
                if self.rect.x in range(i.pos()[0] - i.rect.width, i.pos()[0] + 1):
                    print(4)
                    self.impassible['right'] = False
                    # continue
        elif len(other) == 1:
            if pygame.sprite.spritecollide(self, enemies, False):
                for i in enemies:
                    if self.rect.y in range(i.pos()[1] - i.rect.height, i.pos()[1] + 1):
                        self.impassible['down'] = False
                        print(1)
                        # continue
                    # if i.pos()[0] == self.rect.x and i.pos()[1] < self.rect.y:
                    if self.rect.y in range(i.pos()[1], i.pos()[1] + height + 1):
                        self.impassible['up'] = False
                        print(2)
                        # continue
                    # if i.pos()[0] > self.rect.x and i.pos()[1] == self.rect.y:
                    if self.rect.x in range(i.pos()[0], i.pos()[0] + i.rect.width + 1):
                        self.impassible['left'] = False
                        print(3)
                        # continue
                    # if i.pos()[0] < self.rect.x and i.pos()[1] == self.rect.y:
                    if self.rect.x in range(i.pos()[0] - i.rect.width, i.pos()[0] + 1):
                        print(4)
                        self.impassible['right'] = False
                        # continue
        if self.impassible[next_pos]:
            if self.direction == next_pos:
                self.rect = self.rect.move(*direct)
        self.image = self.images[next_pos]
        self.direction = next_pos
        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect.height = 65
        self.rect.width = 65
        #  проверить по координатам


# создание класса пули
class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bullet.png'), (10, 20))

    # группа спрайтов, позиция, направление, чья пуля(врага, игрока)
    def __init__(self, group, pos, directon, side):
        super().__init__(group)
        # присваивание картинки спрайту
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.images = {
            'up': self.image,
            'down': pygame.transform.rotate(self.image, 180),
            'right': pygame.transform.rotate(self.image, 270),
            'left': pygame.transform.rotate(self.image, 90)
        }

        # переменная для работы перемещения
        self.vectors = {
            'up': (0, -10),
            'down': (0, 10),
            'left': (-10, 0),
            'right': (10, 0)

        }
        self.direction = directon
        self.fly_vector = self.vectors[directon]
        self.mask = pygame.mask.from_surface(self.image)

        # переменная скорости
        self.speed = 0

        # корректировка начальной позиции снаряда
        corr_x = self.rect.width
        corr_y = self.rect.height

        # здесь надо сделать вылет пули
        # из соответсвтвующей точки

        # corr_x, corr_y = coor[self.direction]
        self.rect.x = pos[0] + pos[2] // 2 - 5
        self.rect.y = pos[1] + pos[3] // 2 - 5

        # звуковое оформление сделаем позже
        self.sound = None
        side.add(self)

    # стандартный метод движения пули
    # летит в одном направлении
    def update(self):
        if pygame.sprite.spritecollide(self, walls, False):
            try:
                enother = pygame.sprite.spritecollideany(self, walls, False)
                if enother.type == 'brick' or enother.type == 'steel':
                    global player_shot
                    player_shot = False
                    # pygame.sprite.spritecollideany(self, walls).damage()
                    self.kill()
                    enother.damage(self.direction)
                    # create_particles(enother.pos())
            except Exception:
                pass
        if pygame.sprite.spritecollideany(self, enemies, False):
            enother = pygame.sprite.spritecollideany(self, enemies, False)
            player_shot = False
            enother.explose()
            self.kill()
        if pygame.sprite.spritecollide(self, flags, False):
            enother = pygame.sprite.spritecollide(self, flags, False)
            for i in enother:
                try:
                    print('ok')
                    i.defeat()
                except Exception:
                    pass
        self.corr_im(self.direction)
        self.rect = self.rect.move(self.fly_vector)

    # корректировка картинки пули
    def corr_im(self, direct):
        # print(direct)

        self.image = self.images[direct]
        self.mask = pygame.mask.from_surface(self.image)
        self.fly_vector = self.vectors[direct]


class Wall(pygame.sprite.Sprite):

    def __init__(self, def_group, pos, group, wall_type='Brick'):
        super().__init__(def_group)
        group.add(self)
        self.types = {
            'brick': load_image('brick.png'),
            'steel': pygame.transform.scale(load_image('steel.png'), (65, 65)),
            'impassable': pygame.transform.scale(load_image('impassable.png'), (65, 65)),
            'leaves': pygame.transform.scale(load_image('leaves.png'), (65, 65))
        }
        self.type = wall_type
        self.image = self.types[wall_type]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mask = pygame.mask.from_surface(self.image)
        self.damages = {
            'up': 0,
            'down': 0,
            'left': 0,
            'right': 0
        }

        if wall_type == 'brick':
            self.breakable = True
            self.condition = 4
        else:
            self.breakable = False

        if wall_type == 'leaves':
            self.impass = True
        else:
            self.impass = False

    def update(self, bull_dir=None):
        # присутствует баг
        # после которого стена ломается после 3 попаданий, а надо с 4

        if self.breakable:
            if bull_dir is not None:
                rev_dir = {
                    'up': 'right',
                    'down': 'up',
                    'left': 'down',
                    'right': 'left'
                }
                bull_dir = rev_dir[bull_dir]
                step = self.rect.width // 5
                if bull_dir == 'up':
                    self.damages[bull_dir] += 1
                    self.damages['right'] += 1
                if bull_dir == 'down':
                    self.damages[bull_dir] += 1
                if bull_dir == 'left':
                    self.damages[bull_dir] += 1
                    self.damages['down'] += 1
                if bull_dir == 'right':
                    self.damages[bull_dir] += 1
                self.condition -= 1
            if self.condition <= 3 and bull_dir is not None:
                # self.image = pygame.transform.scale(self.image, (self.rect.width, 40))
                x = self.rect.x
                y = self.rect.y
                self.image = pygame.transform.scale(self.image, (
                    self.rect.width - self.damages['down'] * step, self.rect.height - self.damages['right'] * step))
                self.rect = self.image.get_rect()
                self.rect.x = x + self.damages['left'] * step
                self.rect.y = y + self.damages['up'] * step
                self.mask = pygame.mask.from_surface(self.image)
            elif self.condition == 0:
                print('kill')
                self.kill()

    def pos(self):
        return self.rect.x, self.rect.y

    def damage(self, direction):
        if self.breakable:
            self.update(direction)


class EnemyTank(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('enemy.png'), (65, 65))

    def __init__(self, def_group, group, startpos=None):
        super().__init__(def_group)

        self.image = EnemyTank.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Переменная отвечающая за напрваление движения
        # И положение картинки
        self.direction = 'up'
        self.images = {
            'up': self.image,
            'down': pygame.transform.rotate(self.image, 180),
            'right': pygame.transform.rotate(self.image, 270),
            'left': pygame.transform.rotate(self.image, 90)
        }

        # пока не будет музыки передвижения
        # добавим ближе к завершению
        # добавлять ли звуки к танкам врагов????????
        self.sound = None

        # создание маски
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = startpos[0]
        self.rect.y = startpos[1]

        # переменные для жизней и кол-ва ранений
        self.wounds = 1  # ранения
        self.lifes = 3  # жизни
        group.add(self)

        self.time = 0
        #
        # надо добавить метод спавна танка на позиции
        #
        self.res_pos = startpos

    def explose(self):
        self.wounds -= 1
        if self.wounds == 0:
            self.image = pygame.transform.scale(load_image('explosion.png'), (65, 65))

            #
            # Добавить анимацию взрыва
            #
            self.lifes -= 1
            clock.tick(FPS)
            if self.lifes == 0:
                self.kill()

        if self.wounds == 0:
            self.spawn()

        # метод респавна танка

    def spawn(self):
        self.image = self.images[self.direction]
        self.rect.x, self.rect.y = (random.randint(100, 200), random.randint(250, 300))
        self.wounds = 1

        # метод для возпращения позиции(пока не используется)

    def pos(self):
        return self.rect.x, self.rect.y

        # движение танка игрока

    def move(self, direct):
        next_pos = direct[-1]
        direct = direct[0]
        self.direction = next_pos
        self.mask = self.mask = pygame.mask.from_surface(self.images[next_pos])
        self.image = self.images[next_pos]
        if not pygame.sprite.spritecollide(self, players, False):

            if not pygame.sprite.spritecollide(self, walls, False):
                self.rect = self.rect.move(*direct)
                self.time += 20
                if self.time >= 2000:
                    x = random.choice([-5, 0, 5])
                    y = 0
                    if x == 0:
                        y = random.choice([-5, 0, 5])

                #  проверить по координатам
                #  передвижение танка на 4 флага
                #  создать функцию определения направления
                #  Актуальные задачи:
                #  перемещение вблизи стен
                #  отрисовка стены и её разрушение
                #  респаунн такнков
                #  простенький "ИИ" на рандомах
                #


class Leaves(Wall):
    image = pygame.transform.scale(load_image('leaves.png'), (65, 65))

    def __init__(self, all_group, pos, group):
        super().__init__(all_group, pos, leaves, 'leaves')
        self.image = Leaves.image
        group.add(self)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class MainFlag(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('Flag.png'), (65, 65))

    def __init__(self, group, pos, gr):
        super().__init__(group)
        self.image = MainFlag.image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.lifes = 1
        gr.add(self)

    def defeat(self):
        self.lifes -= 1
        self.image = load_image('defeat.png')
        sec = 0
        pygame.quit()


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


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(game_over=False):
    WIDTH = 400
    HEIGHT = 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    FPS = 50
    clock = pygame.time.Clock()
    COLOR_B = (0, 0, 0)
    COLOR_W = (255, 255, 255)

    screen.fill((255, 255, 255))
    x = WIDTH // 10
    y = -HEIGHT
    # переделать самому тему с тестом
    # сделать кнопки, тупо координаты
    run = True

    while run:
        # screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(WIDTH // 8, WIDTH // 8 + 300) and event.pos[1] in range(HEIGHT // 10 * 5,
                                                                                                 HEIGHT // 10 * 5 + 75) and not game_over:
                    if event.button == 1:
                        return
                if event.pos[0] in range(WIDTH // 8, WIDTH // 8 + 300) and event.pos[1] in range(HEIGHT // 10 * 8,
                                                                                                 HEIGHT // 10 * 8 + 75) and not game_over:
                    if event.button == 1:
                        terminate()

            if (event.type == pygame.KEYDOWN or
                event.type == pygame.MOUSEBUTTONDOWN) and game_over:
                game_over = False
                x = WIDTH // 10
                y = -HEIGHT
        if game_over:
            if y + 4 <= HEIGHT // 2 and game_over:
                screen.fill(COLOR_W)
                pygame.draw.rect(screen, COLOR_W, (x, y, 300, 300))
                font = pygame.font.Font(None, 60)
                text = font.render("<<Game Over>>", 1, (0, 255, 0))
                text1 = font.render('press Any key', 1, (0, 255, 0))
                screen.blit(text, (x, y))
                screen.blit(text1, (x, y + 40))
                y += 4
                # print('game_over')

        if y + 4 <= HEIGHT // 8 and not game_over:
            screen.fill(COLOR_W)
            pygame.draw.rect(screen, COLOR_W, (x, y, 300, 300))
            font = pygame.font.Font(None, 60)
            text = font.render("<<<Tanchiki>>>", 1, (0, 255, 0))
            screen.blit(text, (x, y))
            y += 4
        if y + 4 >= HEIGHT // 8 and not game_over:
            color = (0, 0, 0)
            # pygame.draw.rect(screen, (0, 0, 0), (x - 2, 0, 600, 300))
            screen.fill(COLOR_W)
            font = pygame.font.Font(None, 60)
            text = font.render("<<<Tanchiki>>>", 1, (0, 255, 0))
            screen.blit(text, (x, y))
            start_button = pygame.draw.rect(screen, (128, 128, 128), (WIDTH // 8, 0 + HEIGHT // 10 * 5, 300, 75))
            font = pygame.font.Font(None, 40)
            text = font.render('Начать игру', 1, (0, 0, 0))
            screen.blit(text, (WIDTH // 8 + 75, HEIGHT // 10 * 5 + 20))
            exit_button = pygame.draw.rect(screen, (128, 128, 128), (WIDTH // 8, 0 + HEIGHT // 10 * 8, 300, 75))
            font = pygame.font.Font(None, 40)
            text = font.render('Выход', 1, (0, 0, 0))
            screen.blit(text, (WIDTH // 8 + 75, HEIGHT // 10 * 8 + 20))
        pygame.display.flip()
        clock.tick(FPS)


start_screen()

# def game():
width = 800
height = 600

pygame.init()
pygame.key.set_repeat(200, 10)
STEP = 1
height, width = 65 * 15, 65 * 16
screen = pygame.display.set_mode((width, height))

player_shot = False  # флаг-указатель наличия пули игрока на поле

screen_rect = (0, 0, width, height)

running = True
start = False
player = None
while running:
    screen.fill((0, 0, 0))
    if player is None:
        player, x, y = generate_level(load_level('test_level.txt'))
    all_sprites.add(player)
    players.add(player)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            start_screen()
        # if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:

        if event.type == pygame.KEYDOWN:  # Управление нашим танком
            if event.key == pygame.K_UP:
                player.move(((0, -STEP), 'up'))
            if event.key == pygame.K_DOWN:
                player.move(((0, STEP), 'down'))
            if event.key == pygame.K_RIGHT:
                player.move(((STEP, 0), 'right'))
            if event.key == pygame.K_LEFT:
                player.move(((-STEP, 0), 'left'))
            # выстрел пули на пробел
            if event.key == pygame.K_SPACE and not player_shot:
                # if event.key == pygame.K_SPACE:
                bullet = Bullet(all_sprites, player.pos(), player.direction, player_bullets)
                player_shot = True
        # проверка наличия пули на поле
        if player_shot:
            # проверка пули в пределах экрана
            if bullet.rect.x not in range(width) or bullet.rect.y not in range(height):
                bullet.kill()
                player_shot = False
            # clock.tick(30)

        # стандартная отрисовка объектов
        # пуля, такн игрока
    all_sprites.draw(screen)
    players.draw(screen)
    leaves.draw(screen)
    all_sprites.update()
    clock.tick(FPS)
    pygame.display.flip()



pygame.quit()
