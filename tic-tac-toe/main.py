import pygame
from pygame.locals import *

##########################################
# Note:                                  #
# This is the first pygame game I made   #
# without the use of any tutorials or AI #
##########################################

# initialising the game
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# window and background (tic-tac-toe grid)
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background_surf = pygame.image.load('graphics/grid.png').convert_alpha()
background_rect = background_surf.get_rect(center=(300, 300))

# font + text rendering and loading
player_font = pygame.font.SysFont('Comic Sans MS', 170)
title_font = pygame.font.SysFont('Comic Sans MS', 50)
score_font = pygame.font.SysFont('Comic Sans MS', 20)
main_title = title_font.render("Press space to start!", True, "black")
main_title_rect = main_title.get_rect(center=(300, 300))


# function to check for win condition: returns true if tic-tac-toe rules are met.
def win_condition(letter) -> bool:
    for grid_location in range(len(grid)):
        if grid[grid_location] == letter:
            if grid_location == 0 or grid_location == 3 or grid_location == 6:
                if grid[grid_location] == grid[grid_location + 1] == grid[grid_location + 2]:
                    return True
            if grid_location == 0 or grid_location == 1 or grid_location == 2:
                if grid[grid_location] == grid[grid_location + 3] == grid[grid_location + 6]:
                    return True
            if grid_location == 2:
                if grid[grid_location] == grid[grid_location + 2] == grid[grid_location + 4]:
                    return True
            if grid_location == 0:
                if grid[grid_location] == grid[grid_location + 4] == grid[grid_location + 8]:
                    return True
            else:
                return False


# separates window into a 3x3 grid for tic-tac-toe
pos = pygame.Surface((200, 200))
pos_rect = []
i = 0
while i < 9:
    if i < 3:
        pos_rect.append(pos.get_rect(topleft=(0 + (200 * i), 0)))
    elif i < 6:
        pos_rect.append(pos.get_rect(topleft=(0 + (200 * (i - 3)), 200)))
    elif i < 9:
        pos_rect.append(pos.get_rect(topleft=(0 + (200 * (i - 6)), 400)))
    i += 1

# setting up variables and gameplay before the main game loop
x_counter = 0
o_counter = 0
x_surf = player_font.render("X", True, "black")
x_rect = []
o_surf = player_font.render("O", True, "black")
o_rect = []
grid = [0, 0, 0,
        0, 0, 0,
        0, 0, 0]
turn = 1
x_win = False
y_win = False
game_active = False

# game loop
while True:
    # background colour
    WINDOW.fill('white')

    # event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        # active game state: detecting which grid the mouse is clicking on
        if game_active:
            if event.type == MOUSEBUTTONDOWN:
                for i in range(len(pos_rect)):
                    if pos_rect[i].collidepoint(event.pos) and grid[i] == 0:
                        # turn system: x if odd, o if even, appends a new rectangle to a list depending on turn
                        if turn % 2 != 0:
                            if i < 3:
                                x_rect.append(x_surf.get_rect(center=(100 + 200 * i, 100)))
                            elif i < 6:
                                x_rect.append(x_surf.get_rect(center=(100 + 200 * (i - 3), 300)))
                            elif i < 9:
                                x_rect.append(x_surf.get_rect(center=(100 + 200 * (i - 6), 500)))
                            grid[i] = 1
                        else:
                            if i < 3:
                                o_rect.append(o_surf.get_rect(center=(100 + 200 * i, 100)))
                            elif i < 6:
                                o_rect.append(o_surf.get_rect(center=(100 + 200 * (i - 3), 300)))
                            elif i < 9:
                                o_rect.append(o_surf.get_rect(center=(100 + 200 * (i - 6), 500)))
                            grid[i] = 2
                        turn += 1
        else:
            # inactive game state: refreshes variables and starts game on click
            if (event.type == pygame.KEYDOWN and event.key == K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
                x_rect = []
                o_rect = []
                grid = [0, 0, 0,
                        0, 0, 0,
                        0, 0, 0]
                turn = 1
                game_active = True

    # active game state: detects using win_condition function if 'x' or 'o' wins, or draw happens.
    if game_active:
        WINDOW.blit(background_surf, background_rect)
        x_win = win_condition(1)
        y_win = win_condition(2)
        for i in range(len(x_rect)):
            WINDOW.blit(x_surf, x_rect[i])
        for i in range(len(o_rect)):
            WINDOW.blit(o_surf, o_rect[i])
        if 0 in grid:
            game_active = True
        else:
            game_active = False
        if x_win:
            x_counter += 1
            game_active = False
        if y_win:
            o_counter += 1
            game_active = False

    # inactive gae state: main menu and visible score counter
    else:
        WINDOW.blit(main_title, main_title_rect)
        if x_counter != 0 or o_counter != 0:
            score_x = score_font.render(f"crosses: {x_counter}", True, "black")
            score_x_rect = score_x.get_rect(topleft=(0, 0))
            score_o = score_font.render(f"naughts: {o_counter}", True, 'black')
            score_o_rect = score_o.get_rect(topright=(600, 0))
            WINDOW.blit(score_x, score_x_rect)
            WINDOW.blit(score_o, score_o_rect)

    # display refresh (60hz)
    pygame.display.update()
    clock.tick(60)
