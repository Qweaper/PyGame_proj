import os
import random

import pygame

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
height, width = 500, 500
screen = pygame.display.set_mode((width, height))

player1_shot = False  # флаг-указатель наличия пули игрока на поле

screen_rect = (0, 0, width, height)


# функция загрузки изображения

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

    def __init__(self, def_group, group, startpos=None):
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
        self.rect.x = width // 2
        self.rect.y = height // 2
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
        return self.rect.x, self.rect.y

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
        corr_x = player1.rect.width // 2 - 5
        corr_y = player1.rect.height // 2 - 5

        # здесь надо сделать вылет пули
        # из соответсвтвующей точки

        # corr_x, corr_y = coor[self.direction]
        self.rect.x = pos[0] + corr_x
        self.rect.y = pos[1] + corr_y

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
                    global player1_shot
                    player1_shot = False
                    # pygame.sprite.spritecollideany(self, walls).damage()
                    self.kill()
                    enother.damage(self.direction)
                    # create_particles(enother.pos())
            except Exception:
                pass
        if pygame.sprite.spritecollideany(self, enemies, False):
            enother = pygame.sprite.spritecollideany(self, enemies, False)
            player1_shot = False
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
        while sec != 2:
            sec += clock.tick(FPS)
        pygame.quit()

Flag = MainFlag(all_sprites, (100, 400), flags)
leaves_wall = Wall(all_sprites, (100, 100), leaves, 'leaves')
enemy = EnemyTank(all_sprites, enemies, (100, 300))
wall = Wall(all_sprites, (400, 250), walls, 'brick')
unbreak_wall = Wall(all_sprites, (300, 100), walls, 'steel')
water_wall = Wall(all_sprites, (100, 200), walls, 'impassable')

player1 = PlayerTank(all_sprites, players)
running = True
FPS = 50
while running:
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:  # Управление нашим танком
            if event.key == pygame.K_UP:
                player1.move(((0, -STEP), 'up'))
            if event.key == pygame.K_DOWN:
                player1.move(((0, STEP), 'down'))
            if event.key == pygame.K_RIGHT:
                player1.move(((STEP, 0), 'right'))
            if event.key == pygame.K_LEFT:
                player1.move(((-STEP, 0), 'left'))
            # выстрел пули на пробел
            if event.key == pygame.K_SPACE and not player1_shot:
                # if event.key == pygame.K_SPACE:
                bullet = Bullet(all_sprites, player1.pos(), player1.direction, player_bullets)
                player1_shot = True

    # проверка наличия пули на поле
    if player1_shot:
        # проверка пули в пределах экрана
        if bullet.rect.x not in range(width) or bullet.rect.y not in range(height):
            bullet.kill()
            player1_shot = False
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
