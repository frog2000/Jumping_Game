# <a href="https://www.flaticon.com/free-icons/cactus" title="cactus icons">Cactus icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/coin" title="coin icons">Coin icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/rock" title="rock icons">Rock icons created by Icongeek26 - Flaticon</a>
# Dino by MADNES8
# <a href="https://www.flaticon.com/free-icons/cloud" title="cloud icons">Cloud icons created by vectorspoint - Flaticon</a>

import pygame
from pygame.sprite import Group
import sys
from game_settings import Settings
from sprites import Dino, Cactus, Rock, Coin, Cloud
import game_func
import os


def update_screen():
    # screen.blit(settings.background, (0, 0))
    pass


def run_game():
    pygame.init()
    settings = Settings()

    screen = pygame.display.set_mode((settings.window_width, settings.window_height))
    pygame.display.set_caption("Chrome Dino Game")
    program_icon = pygame.image.load_extended(os.path.join("images", "dino1.png"))
    pygame.display.set_icon(program_icon)

    jump_sound = os.path.abspath(os.path.join("sounds", "jump.wav"))
    win_sound = os.path.abspath(os.path.join("sounds", "win.wav"))
    crash_sound = os.path.abspath(os.path.join("sounds", "crash.wav"))


    clock = pygame.time.Clock()


    dino = Dino(screen, settings)
    # cactus = Cactus(screen, settings)
    # rock = Coin(screen, settings)

    obstacle_classes = [Cactus, Rock]
    obstacles = Group()
    coins = Group()
    clouds = Group()
    allow_ground_object = True
    counter = 0


    while True:
        # clock the game to the specific fps
        clock.tick(settings.fps)
        
        screen.blit(settings.background, (0,0))
        game_func.check_events(dino, jump_sound)

        if allow_ground_object:
            if game_func.generate_object(coins, Coin, screen, settings, settings.prize_generation_probability):
                allow_ground_object = False
                counter = 0

        for obstacle_class in obstacle_classes:
            if not allow_ground_object:
                break
            if game_func.generate_object(obstacles, obstacle_class, screen, settings, settings.obstacle_generation_probability):
                allow_ground_object = False
                counter = 0
                break


        game_func.generate_object(clouds, Cloud, screen, settings, settings.cloud_generation_probability)

        if counter <= 30:
            counter += 1
        else:
            allow_ground_object = True


        dino.update()
        dino.blit_sprite()
        dino.progress_animation()  # go to the next "frame" on the sprite sheet


        game_func.update_objects(obstacles)
        game_func.update_objects(coins)
        game_func.update_objects(clouds)

        game_func.check_collisions(dino, obstacles, coins, win_sound, crash_sound)



        pygame.display.flip()
        #
        # sub = screen.subsurface(screen.get_rect())
        # pygame.image.save(sub, "screenshot.jpg")


if __name__ == '__main__':
    run_game()
