import pygame
import sqlite3
import random
import sys
import start_page as sp
import profile_page as pp
import category_page as cp
import quiz_page as qp
import quiz_result_page as qrp


pygame.init()

WIDTH,HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Quiz")


def main():
    state = 'start'
    login_data = None
    result = None

    while True:

        if state == 'quit':
            pygame.quit()
            sys.exit()

        elif state == 'start':
            state, login_data = sp.draw_start_page(screen, state)

        elif state == 'profile':
            state = pp.draw_profile_page(screen, state, login_data)

        elif state == 'category':
            state = cp.draw_category_page(screen, state)

        elif state == 'quiz':
            state, result = qp.draw_quiz_page(screen, state)

        elif state == 'quiz_result':
            state = qrp.draw_quiz_result_page(screen, state, result)


if __name__ == "__main__":
    main()
