import pygame
import os

pygame.init()

all_sprites = pygame.sprite.Group()
players = pygame.sprite.Group()

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
        self.x = None
        self.y = None
        self.image = PlayerTank.image
        self.rect = self.image.get_rect()

        # Переменная отвечающая за напрваление движения
        # И положение картинки
        self.direction = 'up'
        self.images = {
            'up': self.image,
            'down': pygame.transform.rotate(self.image, 180),
            'left': pygame.transform.rotate(self.image, 270),
            'right': pygame.transform.rotate(self.image, 90)
        }

        # пока не будет музыки передвижения
        # добавим ближе к завершению
        self.sound = None

        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = width // 2
        self.rect.y = height // 2
        players.add(self)

    def move(self, direct):
        next_pos = direct[-1]
        direct = direct[0]

        self.mask = self.mask = pygame.mask.from_surface(self.images[next_pos])
        self.image = self.images[next_pos]
        self.rect = self.rect.move(*direct)


player1 = PlayerTank(all_sprites)
running = True
while running:
    screen.fill((255, 255, 255))
    all_sprites.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: # Управление нашим танком
            if event.key == pygame.K_UP:
                player1.move(((0, -5), 'up'))
            if event.key == pygame.K_DOWN:
                player1.move(((0, 5), 'down'))
            if event.key == pygame.K_RIGHT:
                player1.move(((5, 0), 'left'))
            if event.key == pygame.K_LEFT:
                player1.move(((-5, 0), 'right'))

    all_sprites.draw(screen)
    all_sprites.update()
    players.draw(screen)

    pygame.display.flip()

pygame.quit()
