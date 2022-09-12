import math

import numpy
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
RAY_JUMP = 0.1
RAY_DEPTH = 16

MOVE_SPEED = 0.8
ROTATE_SPEED = 0.1


class Player:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.angle = 0


class Window:
    def __init__(self, width, height, title=None):
        pygame.init()
        self.surface = pygame.display.set_mode((width, height))
        if title is not None:
            pygame.display.set_caption(title)

    def update(self, screen):
        pygame.surfarray.blit_array(self.surface, screen)
        pygame.display.flip()

    def quit(self):
        pygame.quit()


class Input:
    def __init__(self):
        self.quit = False
        self.forward = 0
        self.rotate = 0

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

        keys = pygame.key.get_pressed()

        self.rotate = 0
        if keys[pygame.K_LEFT]:
            self.rotate = -1
        if keys[pygame.K_RIGHT]:
            self.rotate = 1

        self.forward = 0
        if keys[pygame.K_UP]:
            self.forward = 1
        if keys[pygame.K_DOWN]:
            self.forward = -1


class Game:
    def __init__(self):
        self.window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Wolfenpyein 3D")
        self.screen = numpy.array([[(0, 0, 0)] * SCREEN_HEIGHT] * SCREEN_WIDTH)

        player_index = MAP.find(PLAYER)
        px = player_index % MAP_WIDTH + 0.5
        py = player_index // MAP_WIDTH + 0.5
        self.player = Player(px, py)

        self.input = Input()

    def run(self):
        self.quit = False
        while not self.quit:
            self.update()
            self.render()
        self.window.quit()

    def update(self):
        self.input.update()

        if self.input.quit:
            self.quit = True

        self.player.angle += self.input.rotate * ROTATE_SPEED

        move_x, move_y = self.player.x, self.player.y
        move_x += math.cos(self.player.angle) * self.input.forward * MOVE_SPEED
        move_y += math.sin(self.player.angle) * self.input.forward * MOVE_SPEED

        if MAP[int(move_y) * MAP_WIDTH + int(move_x)] != WALL:
            self.player.x, self.player.y = move_x, move_y

    def render(self):
        for x in range(SCREEN_WIDTH):
            ray_angle = (self.player.angle - FOV / 2) + (x / SCREEN_WIDTH) * FOV
            dx = math.cos(ray_angle)
            dy = math.sin(ray_angle)

            hit_wall = False
            dist_to_wall = 0
            while not hit_wall and dist_to_wall < RAY_DEPTH:
                dist_to_wall += RAY_JUMP
                ray_x = int(self.player.x + dx * dist_to_wall)
                ray_y = int(self.player.y + dy * dist_to_wall)
                if MAP[ray_y * MAP_WIDTH + ray_x] == WALL:
                    hit_wall = True

            ceiling = (SCREEN_HEIGHT / 2) - SCREEN_HEIGHT / dist_to_wall
            floor = SCREEN_HEIGHT - ceiling

            for y in range(SCREEN_HEIGHT):
                if y < ceiling:
                    fade = int(255 * (1 - (y / (SCREEN_HEIGHT / 2))))
                    col = (0, 0, fade)
                elif y >= ceiling and y <= floor:
                    fade = int(255 * max(0, 1 - dist_to_wall / RAY_DEPTH))
                    col = (0, fade, 0)
                else:
                    fade = int(255 * (y - SCREEN_HEIGHT / 2) / (SCREEN_HEIGHT / 2))
                    col = (fade, 0, 0)
                self.screen[x][y] = col

        self.window.update(self.screen)


if __name__ == "__main__":
    Game().run()
