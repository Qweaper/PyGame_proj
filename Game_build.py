import os
import random
import sys
import time
import pygame

from tank import PlayerTank, Bullet, Wall, EnemyTank, Leaves, MainFlag

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()
leaves = pygame.sprite.Group()
flags = pygame.sprite.Group()
clock = pygame.time.Clock()
spawns = pygame.sprite.Group()
FPS = 50
size = 30
pygame.init()


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
    image = pygame.transform.scale(load_image('tank.png'), (size, size))

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
            'down': pygame.transform.scale(pygame.transform.rotate(self.image, 180), (size, size)),
            'right': pygame.transform.scale(pygame.transform.rotate(self.image, 270), (size, size)),
            'left': pygame.transform.scale(pygame.transform.rotate(self.image, 90), (size, size))
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

    def update(self):
        if pygame.sprite.spritecollide(self, walls, False):
            other = pygame.sprite.spritecollide(self, walls, False)
            x = self.rect.x
            y = self.rect.y
            if self.direction == 'up':
                j = y // size
                self.rect.y = size * (j + 1)
            if self.direction == 'down':
                j = (y + self.rect.height) // size
                self.rect.y = size * (j - 1)
            if self.direction == 'left':
                i = x // size
                self.rect.x = size * (i + 1)
            if self.direction == 'right':
                i = x // size
                self.rect.x = size + self.rect.width * (i - 1)

    # метод взрыва
    def explose(self):
        self.wounds -= 1
        if self.wounds == 0:
            self.lifes -= 1
            clock.tick(FPS)
            self.spawn()

        if self.lifes == 0:
            global player
            player = None
            self.kill()
            start_screen(True)

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
                # if i.pos()[0] == self.rect.x and i.pos()[1] < self.rect.y:
                if self.rect.y in range(i.pos()[1], i.pos()[1] + height + 1):
                    self.impassible['up'] = False
                    # continue
                # if i.pos()[0] > self.rect.x and i.pos()[1] == self.rect.y:
                if self.rect.x in range(i.pos()[0], i.pos()[0] + i.rect.width + 1):
                    self.impassible['left'] = False
                    # continue
                # if i.pos()[0] < self.rect.x and i.pos()[1] == self.rect.y:
                if self.rect.x in range(i.pos()[0] - i.rect.width, i.pos()[0] + 1):
                    self.impassible['right'] = False
        if pygame.sprite.spritecollide(self, enemies, False):
            for i in enemies:
                if self.rect.y in range(i.pos()[1] - i.rect.height, i.pos()[1] + 1):
                    self.impassible['down'] = False
                    # continue
                # if i.pos()[0] == self.rect.x and i.pos()[1] < self.rect.y:
                if self.rect.y in range(i.pos()[1], i.pos()[1] + height + 1):
                    self.impassible['up'] = False
                    # continue
                # if i.pos()[0] > self.rect.x and i.pos()[1] == self.rect.y:
                if self.rect.x in range(i.pos()[0], i.pos()[0] + i.rect.width + 1):
                    self.impassible['left'] = False
                    # continue
                # if i.pos()[0] < self.rect.x and i.pos()[1] == self.rect.y:
                if self.rect.x in range(i.pos()[0] - i.rect.width, i.pos()[0] + 1):
                    self.impassible['right'] = False
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
        self.rect.height = size
        self.rect.width = size
        #  проверить по координатам


# создание класса пули
class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bullet.png'), (size // 5, size // 5 * 2))

    # группа спрайтов, позиция, направление, чья пуля(врага, игрока)
    def __init__(self, group, pos, directon, side_group, side):
        super().__init__(group)
        # присваивание картинки спрайту
        self.side = side
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
        self.rect.x = pos[0] + pos[2] // 2
        self.rect.y = pos[1] + pos[3] // 2

        # звуковое оформление сделаем позже
        self.sound = None
        side_group.add(self)

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
        if pygame.sprite.spritecollideany(self, enemies, False) and self.side == 'player':
            enother = pygame.sprite.spritecollideany(self, enemies, False)
            player_shot = False
            enother.explose()
            self.kill()
        if pygame.sprite.spritecollide(self, flags, False):
            enother = pygame.sprite.spritecollide(self, flags, False)
            for i in enother:
                try:
                    i.defeat()
                except Exception:
                    pass
        if pygame.sprite.spritecollideany(self, players, False) and self.side == 'enemy':
            enother = pygame.sprite.spritecollideany(self, players, False)
            player_shot = False
            enother.explose()
            self.kill()
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
            'brick': pygame.transform.scale(load_image('brick.png'), (size, size)),
            'steel': pygame.transform.scale(load_image('steel.png'), (size, size)),
            'impassable': pygame.transform.scale(load_image('impassable.png'), (size, size)),
            'leaves': pygame.transform.scale(load_image('leaves.png'), (size, size))
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
                self.kill()

    def pos(self):
        return self.rect.x, self.rect.y

    def damage(self, direction):
        if self.breakable:
            self.update(direction)


class EnemyTank(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('enemy.png'), (size, size))

    def __init__(self, def_group, group, startpos=None):
        super().__init__(def_group)

        self.image = EnemyTank.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        # Переменная отвечающая за напрваление движения
        # И положение картинки
        self.shoot = False
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
        self.shoot_time = 0
        #
        # надо добавить метод спавна танка на позиции
        #
        self.res_pos = startpos

    def explose(self):
        self.wounds -= 1
        if self.wounds == 0:
            self.image = pygame.transform.scale(load_image('explosion.png'), (size, size))

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
        self.rect.x, self.rect.y = self.res_pos
        self.wounds = 1
        self.time = 0
        # метод для возпращения позиции(пока не используется)

    def pos(self):
        return self.rect.x, self.rect.y, self.rect.width, self.rect.height

    def update(self):
        self.time += time.clock()
        self.shoot_time += time.clock()
        if self.time // (random.randint(2, 4) * 1000) >= 1:
            self.choose_path()
            self.time = 0
        if self.shoot_time // (1000 * random.randint(2, 4)) >= 1:
            bul = Bullet(all_sprites, self.pos(), self.direction, enemy_bullets, 'enemy')
            self.shoot = True
            self.shoot_time = 0
        else:
            self.shoot = False
        if self.direction == 'up':
            self.move(((0, -STEP), self.direction))
        if self.direction == 'down':
            self.move(((0, STEP), self.direction))
        if self.direction == 'left':
            self.move(((-STEP, 0), self.direction))
        if self.direction == 'right':
            self.move(((STEP, 0), self.direction))
        if pygame.sprite.spritecollide(self, walls, False):
            other = pygame.sprite.spritecollide(self, walls, False)
            x = self.rect.x
            y = self.rect.y
            if self.direction == 'up':
                j = y // size
                self.rect.y = size * (j + 1)
            if self.direction == 'down':
                j = (y + self.rect.height) // size
                self.rect.y = size * (j - 1)
            if self.direction == 'left':
                i = x // size
                self.rect.x = size * (i + 1)
            if self.direction == 'right':
                i = x // size
                self.rect.x = size + self.rect.width * (i - 1)

    def choose_path(self, code='udlr'):
        if code == 'udlr':
            randomizer = random.randint(1, 101)
        elif code == 'udl':
            randomizer = random.randint(1, 76)
        elif code == 'udr':
            randomizer = random.randint(1, 76)
            if 75 < randomizer < 89:
                randomizer = 60
        elif code == 'ulr':
            randomizer = random.randint(26, 101)
            if 25 < randomizer <= 50:
                randomizer = 25
        elif code == 'dlr':
            randomizer = random.randint(51, 101)
        if randomizer <= 25:
            self.direction = 'up'
        elif 25 < randomizer <= 50:
            self.direction = 'down'
        elif 50 < randomizer < 76:
            self.direction = 'left'
        else:
            self.direction = 'right'

    # движение танка враа

    def move(self, direct):
        next_pos = direct[-1]
        direct = direct[0]
        rev_dir = {
            'up': 'right',
            'down': 'left',
            'left': 'up',
            'right': 'down'
        }
        bull_dir = rev_dir[next_pos]
        self.direction = next_pos
        self.mask = self.mask = pygame.mask.from_surface(self.images[bull_dir])
        self.image = self.images[bull_dir]
        if not pygame.sprite.spritecollide(self, players, False):

            if not pygame.sprite.spritecollide(self, walls, False):
                self.rect = self.rect.move(*direct)

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
    image = pygame.transform.scale(load_image('leaves.png'), (size, size))

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
    image = pygame.transform.scale(load_image('Flag.png'), (size, size))

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
        for i in all_sprites:
            i.kill()
        global player
        player = None
        start_screen(True)


class Spawn(pygame.sprite.Sprite):
    image = load_image('spawn_point.png')

    def __init__(self, def_group, pos, limit):
        super().__init__(def_group)
        self.image = pygame.transform.scale(Spawn.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.limit = limit
        self.time = 0
        spawns.add(self)

    def update(self):
        self.time += time.clock()
        if self.time // 10000 >= 1:
            self.time = 0
            if self.limit != 0:
                EnemyTank(all_sprites, enemies, (self.rect.x, self.rect.y))
                self.limit -= 1


def load_level(filename='level_1'):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_width = tile_height = size


def generate_level(level='level_1'):
    new_player, x, y = None, None, None
    global matrix
    matrix = [[0 for _ in range(len(level))] for _ in range(len(level))]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == 'W':
                Wall(all_sprites, (y * size, x * size), walls, 'impassable')
                matrix[y][x] = 1
            elif level[y][x] == '#':
                Wall(all_sprites, (y * size, x * size), walls, 'steel')
                matrix[y][x] = 1
            elif level[y][x] == 'F':
                MainFlag(all_sprites, (y * size, x * size), flags)
            elif level[y][x] == 'L':
                Wall(all_sprites, (y * size, x * size), leaves, 'leaves')
            elif level[y][x] == '*':
                Wall(all_sprites, (y * size, x * size), walls, 'brick')
                matrix[y][x] = 1
            elif level[y][x] == 'E':
                EnemyTank(all_sprites, enemies, (y * size, x * size))
            elif level[y][x] == '@':
                new_player = PlayerTank(all_sprites, players, (y * size, x * size))
            elif level[y][x] in '123456789':
                Spawn(all_sprites, (y * size, x * size), int(level[y][x]))
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
    pygame.mixer_music.load('data/main_menu.mp3')
    pygame.mixer_music.play()
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
                        pygame.mixer_music.pause()
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


while True:
    start_screen()

    # def game():
    width = 800
    height = 600

    pygame.key.set_repeat(200, 10)
    STEP = 1
    # height, width = size * 15, size * 16
    # # height, width = 1000, 1000
    # screen = pygame.display.set_mode((width, height))

    player_shot = False  # флаг-указатель наличия пули игрока на поле

    screen_rect = (0, 0, width, height)

    num_of_enemies = 0
    for i in spawns:
        num_of_enemies += i.limit
    running = True
    start = False
    player = None
    while running:

        if player is None:
            player, x, y = generate_level(load_level())
            height, width = size * 15, size * 16
            # height, width = 1000, 1000
            screen = pygame.display.set_mode((width, height))
            all_sprites.add(player)
            players.add(player)
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # start_screen()
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
                    if len(player_bullets) == 0:
                        bullet = Bullet(all_sprites, player.pos(), player.direction, player_bullets, 'player')
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
