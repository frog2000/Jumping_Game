# <a href="https://www.flaticon.com/free-icons/cactus" title="cactus icons">Cactus icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/coin" title="coin icons">Coin icons created by Freepik - Flaticon</a>
# <a href="https://www.flaticon.com/free-icons/rock" title="rock icons">Rock icons created by Icongeek26 - Flaticon</a>
# Dino by MADNES8
# <a href="https://www.flaticon.com/free-icons/cloud" title="cloud icons">Cloud icons created by vectorspoint - Flaticon</a>

import pygame
from pygame.sprite import Group
import os
import numpy as np
import sys
from game_settings import Settings
from sprites import Dino, Cactus, Rock, Coin, Cloud
from game_scores import GameScores
import game_func
import neural_network


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.window_width, settings.window_height))
    scores = GameScores(settings, screen)

    pygame.display.set_caption("Jumping Game")
    program_icon = pygame.image.load_extended(os.path.join("images", "cactus.png"))
    pygame.display.set_icon(program_icon)

    jump_sound = os.path.abspath(os.path.join("sounds", "jump.wav"))
    win_sound = os.path.abspath(os.path.join("sounds", "win.wav"))
    crash_sound = os.path.abspath(os.path.join("sounds", "crash.wav"))

    clock = pygame.time.Clock()
    dino = Dino(screen, settings)
    obstacle_classes = [Cactus, Rock]
    obstacles = Group()
    coins = Group()
    clouds = Group()
    counter = 0
    loops = 0

    nn_model = neural_network.create_nn_model(2, 2)

    while True:
        screen.blit(settings.background, (0,0))
        game_func.check_events(dino, jump_sound, settings, scores, obstacles)

        distance_to_obstacle = game_func.calculate_distance_to_obstacle(dino, obstacles, settings)

        nn_model_input = np.array([settings.object_velocity, distance_to_obstacle]).reshape(1,-1)

        nn_prediction = nn_model.predict(nn_model_input, verbose=0)
        print("prediction: ", nn_prediction)

        if nn_prediction[0][1] > nn_prediction[0][0]:
            game_func.initiate_jump(dino, jump_sound, settings, scores, obstacles)

        if counter >= settings.obstacle_interval:
            if game_func.generate_object(coins, Coin, screen, settings, settings.prize_generation_probability):
                counter = 0
            else:
                for obstacle_class in obstacle_classes:
                    if game_func.generate_object(obstacles, obstacle_class, screen, settings,
                                                 settings.obstacle_generation_probability):
                        counter = 0
                        break
        game_func.generate_object(clouds, Cloud, screen, settings, settings.cloud_generation_probability)
        counter += 1

        game_func.update_objects(obstacles, scores)
        game_func.update_objects(coins, scores)
        game_func.update_objects(clouds, scores)

        dino.update()
        dino.blit_sprite()
        dino.advance_animation()  # go to the next "frame" on the sprite sheet
        scores.blit_scoreboards()

        game_func.check_collisions(dino, obstacles, coins, win_sound, crash_sound, settings, scores)

        # clock the game to the specific fps
        clock.tick(settings.fps)
        pygame.display.flip()
        settings.increase_difficulty()

        print("lenght:", len(scores.success), "loops: ", loops)
        if len(scores.success) >= 10 and loops % 500 == 0:
            nn_model = neural_network.train_nn_model(nn_model, scores.velocities, scores.distances, scores.success)

        loops += 1


if __name__ == '__main__':
    run_game()
