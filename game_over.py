import pygame
import quiz_lib as qlib
import random
import math
from pygame import mixer

FPS = 30

WIDTH,HEIGHT = 800,600
# Цвета
BLACK = (0, 0, 0)
DARKBLUE = (32, 32, 150)
COLORS = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (190, 0, 0),  # Red
    (0, 190, 0),  # Green
    (0, 0, 190),  # Blue
    (190, 190, 0),  # Yellow
    (190, 0, 190),  # Magenta
    (0, 190, 190)  # Cyan
]


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.life = random.randint(50, 100)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1, 8)

    def update(self):
        self.life -= 1
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        self.speed *= 0.95  # Замедление частиц

    def draw(self, screen):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


def draw_game_over_page(screen, state, quiz_set):

    fonts = qlib.create_fonts()
    clock = pygame.time.Clock()
    button_next = qlib.create_button('Узнать результаты', 250, 500, 250, 40, qlib.TEXT_COLOR, font=fonts['font32'])

    particles = []

    CHANGE_COLOR = pygame.USEREVENT + 1
    pygame.time.set_timer(CHANGE_COLOR, 500)
    z = 8
    z = random.randrange(1, 8,1)
    for i in range(0, z):
        x = random.randrange(WIDTH)
        y = random.randrange(HEIGHT)
        color = random.choice(COLORS)
        for _ in range(50):  # Добавляем 50 частиц
            particles.append(Particle(x, y, color))

    mixer.music.load("sound/vyigrysh.mp3")

    # Setting the volume
    mixer.music.set_volume(0.7)

    # Start playing the song
    mixer.music.play()

    while True:
        screen.fill(DARKBLUE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            elif state == 'game_over':
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_next['bt_rect'].collidepoint(event.pos):
                        return 'quiz_result'


            if event.type == CHANGE_COLOR:
                if not mixer.music.get_busy():
                    mixer.music.play()
                z = 8
                z = random.randrange(1,8,1)
                for i in range(0, z):
                    x = random.randrange(WIDTH)
                    y = random.randrange(HEIGHT)
                    color = random.choice(COLORS)
                    for _ in range(50):  # Добавляем 50 частиц
                        particles.append(Particle(x, y, color))

        for particle in particles:
            particle.update()
            particle.draw(screen)

        # Удаляем частицы, которые больше не видны
        particles = [particle for particle in particles if particle.life > 0]

        qlib.draw_text(screen, "Поздравляем!", (170, 50), False, fonts['font48'])

        qlib.draw_button(screen, button_next)

        pygame.display.flip()
        clock.tick(FPS)
