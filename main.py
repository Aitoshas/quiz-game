import pygame
import sqlite3
import random

pygame.init()

WIDTH,HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Quiz")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 32)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

question_text = font.render()
screen.blit(question_text,(100,100))
answer_text = font.render(True, WHITE)





pygame.display.flip()

pygame.quit()
