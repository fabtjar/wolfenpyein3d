import math

import numpy as np
import pygame

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 270
MAP_WIDTH = 20
MAP_HEIGHT = 15

MAP = """
####################
#..................#
#..##..............#
#..#...........#...#
#..#....########...#
#..............#...#
#..................#
#....X.....##......#
#..........##......#
#..................#
#.....#########....#
#............##....#
#.....##...........#
#.....##...........#
####################
""".strip().replace(
    "\n", ""
)
WALL = "#"
EMPTY = "."
PLAYER = "X"

FOV = math.pi / 8
DEPTH = 16
MOVE_SPEED = 0.8
ANGLE_SPEED = 0.1


def run_game():
    pygame.init()
    pygame.display.set_caption("Wolfenpyein 3D")
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.surfarray.pixels2d(window)

    player_map = MAP.find(PLAYER)
    player_x = player_map % MAP_WIDTH + 0.5
    player_y = player_map // MAP_WIDTH + 0.5
    player_angle = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_angle -= ANGLE_SPEED
        if keys[pygame.K_RIGHT]:
            player_angle += ANGLE_SPEED

        move_x, move_y = player_x, player_y

        if keys[pygame.K_UP]:
            move_x += math.cos(player_angle) * MOVE_SPEED
            move_y += math.sin(player_angle) * MOVE_SPEED
        if keys[pygame.K_DOWN]:
            move_x -= math.cos(player_angle) * MOVE_SPEED
            move_y -= math.sin(player_angle) * MOVE_SPEED

        if MAP[int(move_y) * MAP_WIDTH + int(move_x)] != WALL:
            player_x, player_y = move_x, move_y

        for x in range(SCREEN_WIDTH):
            ray_angle = (player_angle - FOV / 2) + (x / SCREEN_WIDTH) * FOV
            dist_to_wall = 0
            hit_wall = False

            eye_x = math.cos(ray_angle)
            eye_y = math.sin(ray_angle)

            while not hit_wall and dist_to_wall < DEPTH:
                dist_to_wall += 0.1
                test_x = int(player_x + eye_x * dist_to_wall)
                test_y = int(player_y + eye_y * dist_to_wall)
                if MAP[test_y * MAP_WIDTH + test_x] == WALL:
                    hit_wall = True

            ceiling = (SCREEN_HEIGHT / 2) - SCREEN_HEIGHT / dist_to_wall
            floor = SCREEN_HEIGHT - ceiling

            for y in range(SCREEN_HEIGHT):
                if y < ceiling:
                    fade = int(255 * (1 - (y / (SCREEN_HEIGHT / 2))))
                    col = fade << 0
                elif y >= ceiling and y <= floor:
                    fade = int(255 * max(0, 1 - dist_to_wall / DEPTH))
                    col = fade << 8
                else:
                    fade = int(255 * (y - SCREEN_HEIGHT / 2) / (SCREEN_HEIGHT / 2))
                    col = fade << 16
                screen[x][y] = col

        pygame.surfarray.blit_array(window, screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_game()
