import os
import sys

import pygame

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 50
clock = pygame.time.Clock()
COLOR_B = (0, 0, 0)
COLOR_W = (255, 255, 255)


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
    screen.fill((255, 255, 255))
    x = WIDTH // 10
    y = -HEIGHT
    # переделать самому тему с тестом
    # сделать кнопки, тупо координаты

    while True:
        # screen.fill((255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.pos[0] in range(WIDTH // 8, WIDTH // 8 + 300) and event.pos[1] in range(HEIGHT // 10 * 5,
                                                                                                 HEIGHT // 10 * 5 + 75) and not game_over:
                    if event.button == 1:
                        return

            elif (event.type == pygame.KEYDOWN or
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

        pygame.display.flip()
        clock.tick(FPS)


start_screen()
