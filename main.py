import pygame
import sys
import start_page as sp
import profile_page as pp
import category_page as cp
import quiz_page as qp
import quiz_result_page as qrp
import game_over as gg


pygame.init()

WIDTH,HEIGHT = 800,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Викторина Зерокодера")


def main():
    state = 'start'
    user_data = None
    quiz_set = None

    while True:

        if state == 'quit':
            pygame.quit()
            sys.exit()

        elif state == 'start':
            state, user_data = sp.draw_start_page(screen, state)

        elif state == 'profile':
            state = pp.draw_profile_page(screen, state, user_data)

        elif state == 'category':
            state, quiz_set = cp.draw_category_page(screen, state)

        elif state == 'quiz':
            state, quiz_set = qp.draw_quiz_page(screen, state, quiz_set, user_data)

        elif state == 'game_over':
            state = gg.draw_game_over_page(screen, state, quiz_set)

        elif state == 'quiz_result':
            state = qrp.draw_quiz_result_page(screen, state, quiz_set)


if __name__ == "__main__":
    main()
