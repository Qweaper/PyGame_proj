import pygame
import os
import random

pygame.init()

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()
walls = pygame.sprite.Group()

clock = pygame.time.Clock()
height, width = 500, 500
screen = pygame.display.set_mode((width, height))

player1_shot = False  # флаг-указатель наличия пули игрока на поле


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

    def __init__(self, group, startpos=None):
        super().__init__(group)
        # self.x = None
        # self.y = None

        # загрузка картинки
        self.image = PlayerTank.image
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
        self.sound = None

        # создание маски
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = width // 2
        self.rect.y = height // 2

        # переменные для жизней и кол-ва ранений
        self.wounds = 1  # ранения
        self.lifes = 3  # жизни
        players.add(self)

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
            clock.tick(1000)
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
        self.direction = next_pos
        self.mask = self.mask = pygame.mask.from_surface(self.images[next_pos])
        self.image = self.images[next_pos]
        if not pygame.sprite.spritecollide(self, walls, False):
            self.rect = self.rect.move(*direct)
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
                    enother.damage()
                    self.kill()
            except Exception:
                pass
        enother = pygame.sprite.spritecollideany(self, enemies, False)
        if enother:
            player1_shot = False
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

    def __init__(self, group, wall_type, pos):
        super().__init__(group)
        walls.add(self)
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

        if wall_type == 'brick':
            self.breakable = True
            self.condition = 4
        else:
            self.breakable = False

        if wall_type == 'leaves':
            self.impass = True
        else:
            self.impass = False

    def update(self):
        if self.breakable:
            if self.condition == 2 and self.breakable:
                self.image = pygame.transform.scale(self.image, (self.rect.width, 40))
                x = self.rect.x
                y = self.rect.y
                self.rect = self.image.get_rect()
                self.rect.x = x
                self.rect.y = y
                self.mask = pygame.mask.from_surface(self.image)
            elif self.condition == 0:
                self.kill()

    def damage(self):
        if self.breakable:
            self.condition -= 1
            self.update()


class EnemyTank(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('enemy.png'), (65, 65))

    def __init__(self, group, startpos=None):
        super().__init__(group)

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
        enemies.add(self)

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
            clock.tick(1000)
            self.kill()

        if self.lifes != 0:
            self.spawn()

        # метод респавна танка

    def spawn(self):
        self.image = self.images[self.direction]
        self.rect.x, self.rect.y = (100, 300)
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


enemy = EnemyTank(all_sprites, (100, 300))
leaves_wall = Wall(all_sprites, 'leaves', (100, 100))
wall = Wall(all_sprites, 'brick', (200, 100))
unbreak_wall = Wall(all_sprites, 'steel', (300, 100))
water_wall = Wall(all_sprites, 'impassable', (100, 200))

player1 = PlayerTank(all_sprites)
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
                player1.move(((0, -5), 'up'))
            if event.key == pygame.K_DOWN:
                player1.move(((0, 5), 'down'))
            if event.key == pygame.K_RIGHT:
                player1.move(((5, 0), 'right'))
            if event.key == pygame.K_LEFT:
                player1.move(((-5, 0), 'left'))
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
    all_sprites.update()
    players.draw(screen)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
