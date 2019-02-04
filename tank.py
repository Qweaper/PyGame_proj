import pygame
import os

pygame.init()

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

clock = pygame.time.Clock()
height, width = 500, 500
screen = pygame.display.set_mode((width, height))


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


class PlayerTank(pygame.sprite.Sprite):
    image = load_image('tank.png')

    def __init__(self, group):
        super().__init__(group)
        # self.x = None
        # self.y = None
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

        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = width // 2
        self.rect.y = height // 2
        players.add(self)

    def pos(self):
        return self.rect.x, self.rect.y

    def move(self, direct):
        next_pos = direct[-1]
        direct = direct[0]
        self.direction = next_pos
        self.mask = self.mask = pygame.mask.from_surface(self.images[next_pos])
        self.image = self.images[next_pos]
        self.rect = self.rect.move(*direct)


class Bullet(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('bullet.png'), (10, 20))

    def __init__(self, group, pos, directon, side):
        super().__init__(group)
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.images = {
            'up': self.image,
            'down': pygame.transform.rotate(self.image, 180),
            'right': pygame.transform.rotate(self.image, 270),
            'left': pygame.transform.rotate(self.image, 90)
        }

        self.vectors = {
            'up': (0, -10),
            'down': (0, 10),
            'left': (-10, 0),
            'right': (10, 0)

        }
        self.direction = directon
        self.fly_vector = self.vectors[directon]
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = 0

        # корректировка начальной позиции снаряда
        corr_x = player1.rect.width // 2 - 5
        corr_y = player1.rect.height // 2 - 5
        coor = {
            'up': (corr_x, 0),
            'down': (corr_x, corr_y * 2),
            'right': (corr_x * 2, corr_y),
            'left': (0, corr_y)

        }

        # здесь надо сделать вылет пули
        # из соответсвтвующей точки
        corr_x, corr_y = coor[self.direction]
        self.rect.x = pos[0] + corr_x
        self.rect.y = pos[1] + corr_y

        # звуковое оформление сделаем позже
        self.sound = None
        side.add(self)

    def update(self):
        # if not pygame.sprite.collide_mask(self.mask, enemies):
        #     global player1_shot
        #     player1_shot = False
        #     pass
        self.corr_im(self.direction)
        self.rect = self.rect.move(self.fly_vector)

    def corr_im(self, direct):
        # print(direct)

        self.image = self.images[direct]
        self.mask = pygame.mask.from_surface(self.image)
        self.fly_vector = self.vectors[direct]


player1 = PlayerTank(all_sprites)
running = True
player1_shot = False
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
            if event.key == pygame.K_SPACE and not player1_shot:
                # if event.key == pygame.K_SPACE:
                bullet = Bullet(all_sprites, player1.pos(), player1.direction, player_bullets)
                player1_shot = True
    if player1_shot:
        if bullet.rect.x not in range(width) or bullet.rect.y not in range(height):
            bullet.kill()
            player1_shot = False
        # clock.tick(30)

    all_sprites.draw(screen)
    all_sprites.update()
    players.draw(screen)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
