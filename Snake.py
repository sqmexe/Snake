import pygame
import sys
import numpy as np
import random
import time

pygame.init()
clock = pygame.time.Clock()

Partikel = 25
WIDTH = Partikel * 27
HEIGHT = Partikel * 23
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font_big = pygame.font.SysFont(None, 80)
font_medium = pygame.font.SysFont(None, 45)
font_small = pygame.font.SysFont(None, 30)

# ---------------- CONTROLS MENU ----------------
def controls_menu():
    while True:
        screen.fill((0, 120, 0))

        title = font_big.render("Controls", True, (255, 255, 255))

        lines = [
            "Arrow Keys = Move Snake",
            "P = Pause / Resume",
            "ESC = Quit Game",
            "",
            "Red Apple = +1 Point",
            "Golden Apple = +5 Points",
            "Golden apple spawns every 5-15 apples",
            "",
            "Death happens when:",
            "- You hit the wall (border)",
        ]

        back_text = font_small.render("Back", True, (255, 255, 255))
        back_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT - 80, 200, 50)

        screen.blit(title, (WIDTH//2 - 150, 50))

        y = 150
        for line in lines:
            text = font_small.render(line, True, (255, 255, 255))
            screen.blit(text, (WIDTH//2 - 200, y))
            y += 35

        pygame.draw.rect(screen, (0, 0, 0), back_rect)
        screen.blit(back_text, (back_rect.x + 75, back_rect.y + 12))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse):
                    return

        clock.tick(60)


# ---------------- START MENU ----------------
def start_menu():
    while True:
        screen.fill((0, 150, 0))

        title = font_big.render("Snake Game", True, (0, 0, 0))
        start_text = font_small.render("Start", True, (255, 255, 255))
        controls_text = font_small.render("Controls", True, (255, 255, 255))
        quit_text = font_small.render("Quit", True, (255, 255, 255))

        title_rect = title.get_rect(center=(WIDTH // 2, 150))
        start_rect = pygame.Rect(WIDTH//2 - 100, 260, 200, 60)
        controls_rect = pygame.Rect(WIDTH//2 - 100, 340, 200, 60)
        quit_rect = pygame.Rect(WIDTH//2 - 100, 420, 200, 60)

        pygame.draw.rect(screen, (0, 0, 0), start_rect)
        pygame.draw.rect(screen, (0, 0, 0), controls_rect)
        pygame.draw.rect(screen, (0, 0, 0), quit_rect)

        screen.blit(title, title_rect)
        screen.blit(start_text, (start_rect.x + 70, start_rect.y + 15))
        screen.blit(controls_text, (controls_rect.x + 55, controls_rect.y + 15))
        screen.blit(quit_text, (quit_rect.x + 70, quit_rect.y + 15))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse):
                    return
                if controls_rect.collidepoint(mouse):
                    controls_menu()
                if quit_rect.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        clock.tick(60)


# ---------------- GAME OVER SCREEN ----------------
def game_over_screen(score):
    while True:
        screen.fill((150, 0, 0))

        over_text = font_big.render("GAME OVER", True, (255, 255, 255))
        score_text = font_medium.render(f"Score: {score}", True, (255, 255, 255))
        restart_text = font_small.render("Restart", True, (255, 255, 255))
        quit_text = font_small.render("Quit", True, (255, 255, 255))

        restart_rect = pygame.Rect(WIDTH//2 - 100, 330, 200, 60)
        quit_rect = pygame.Rect(WIDTH//2 - 100, 410, 200, 60)

        screen.blit(over_text, (WIDTH//2 - 200, 150))
        screen.blit(score_text, (WIDTH//2 - 80, 230))

        pygame.draw.rect(screen, (0, 0, 0), restart_rect)
        pygame.draw.rect(screen, (0, 0, 0), quit_rect)

        screen.blit(restart_text, (restart_rect.x + 60, restart_rect.y + 15))
        screen.blit(quit_text, (quit_rect.x + 70, quit_rect.y + 15))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if restart_rect.collidepoint(mouse):
                    game()
                if quit_rect.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        clock.tick(60)


# ---------------- GAME ----------------
def game():
    Schlange = [[13, 13], [13, 14]]
    apfelCoords = []
    richtung = 0
    anhang = None
    apfelInd = -1
    score = 0
    paused = False

    goldenApple = None
    apples_eaten = 0
    next_golden = random.randint(5, 15)

    def zeichner():
        screen.fill((0, 102, 0))

        for a in apfelCoords:
            c = [a[0] * Partikel, a[1] * Partikel]
            pygame.draw.rect(screen, (255, 0, 0), (c[0], c[1], Partikel, Partikel))

        if goldenApple is not None:
            c = [goldenApple[0] * Partikel, goldenApple[1] * Partikel]
            pygame.draw.rect(screen, (255, 215, 0), (c[0], c[1], Partikel, Partikel))

        Kopf = True
        for x in Schlange:
            c = [x[0] * Partikel, x[1] * Partikel]
            if Kopf:
                pygame.draw.rect(screen, (0, 0, 0), (c[0], c[1], Partikel, Partikel))
                Kopf = False
            else:
                pygame.draw.rect(screen, (47, 79, 79), (c[0], c[1], Partikel, Partikel))

        pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT), 5)

        score_text = font_small.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if paused:
            pause_text = font_big.render("PAUSED", True, (255, 255, 255))
            screen.blit(pause_text, (WIDTH//2 - 150, HEIGHT//2 - 40))

    def apfelCoordsGen():
        while True:
            c = [random.randint(0, 26), random.randint(0, 22)]
            if c not in Schlange and c not in apfelCoords and c != goldenApple:
                return c

    apfelCoords.append(apfelCoordsGen())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_p:
                    paused = not paused

                if not paused:
                    if event.key == pygame.K_UP and richtung != 2:
                        richtung = 0
                    if event.key == pygame.K_RIGHT and richtung != 3:
                        richtung = 1
                    if event.key == pygame.K_DOWN and richtung != 0:
                        richtung = 2
                    if event.key == pygame.K_LEFT and richtung != 1:
                        richtung = 3

        if not paused:
            time.sleep(0.1)

            if anhang:
                Schlange.append(anhang.copy())
                anhang = None
                apfelCoords.pop(apfelInd)

            for i in range(len(Schlange) - 1, 0, -1):
                Schlange[i] = Schlange[i - 1].copy()

            if richtung == 0:
                Schlange[0][1] -= 1
            if richtung == 1:
                Schlange[0][0] += 1
            if richtung == 2:
                Schlange[0][1] += 1
            if richtung == 3:
                Schlange[0][0] -= 1

            if Schlange[0][0] < 0 or Schlange[0][0] > 26 or Schlange[0][1] < 0 or Schlange[0][1] > 22:
                game_over_screen(score)

            for i in range(len(apfelCoords)):
                if apfelCoords[i] == Schlange[0]:
                    anhang = Schlange[-1].copy()
                    apfelInd = i
                    score += 1
                    apples_eaten += 1

                    if apples_eaten >= next_golden and goldenApple is None:
                        goldenApple = apfelCoordsGen()

            if goldenApple is not None and Schlange[0] == goldenApple:
                score += 5
                goldenApple = None
                apples_eaten = 0
                next_golden = random.randint(5, 15)

            if np.random.randint(0, 100) <= 1 or len(apfelCoords) == 0:
                if len(apfelCoords) < 4:
                    apfelCoords.append(apfelCoordsGen())

        zeichner()
        pygame.display.update()
        clock.tick(8)


# ---------------- MAIN ----------------
start_menu()
game()
