# Jumping game similar to the T-Rex Dinosaur Game of the Chrome browser
# with a vanilla NN attached to it
# The character quickly learn how to jump over the obstacles
#
# Game created by Adrian Krzyzanowski
#
# Attributions:
#
# The main character images are used through an open license
# (images downloaded from https://www.gameart2d.com/freebies.html)
#
# Cactus icons created by Freepik - Flaticon (https://www.flaticon.com/free-icons/cactus)
# Coin icons created by Freepik - Flaticon (https://www.flaticon.com/free-icons/coin)
# Rock icons created by Icongeek26 - Flaticon (https://www.flaticon.com/free-icons/rock)
# Cloud icons created by vectorspoint - Flaticon (https://www.flaticon.com/free-icons/cloud)

import pygame
from pygame.sprite import Group
import os
import numpy as np
from game_settings import Settings
from sprites import MainCharacter, Cactus, Rock, Coin, Cloud
from game_scores import GameScores
import game_func
import neural_network


def run_game():
    pygame.init()
    clock = pygame.time.Clock()  # used for regulating the frames per second
    settings = Settings()
    screen = pygame.display.set_mode((settings.window_width, settings.window_height))
    scores = GameScores(settings, screen)

    pygame.display.set_caption("Jumping Game")
    program_icon = pygame.image.load_extended(os.path.join("images", "cactus.png"))
    pygame.display.set_icon(program_icon)

    # load the sounds used by the game
    jump_sound = os.path.abspath(os.path.join("sounds", "jump.wav"))
    win_sound = os.path.abspath(os.path.join("sounds", "win.wav"))
    crash_sound = os.path.abspath(os.path.join("sounds", "crash.wav"))

    main_character = MainCharacter(screen, settings)
    obstacle_classes = [Cactus, Rock]
    obstacles = Group()
    coins = Group()
    clouds = Group()

    nn_model = neural_network.create_nn_model(2, 2)

    obstacle_interval = 0
    loops = 0

    while True:
        screen.blit(settings.background, (0, 0))  # draw the screen
        game_func.check_events(main_character, jump_sound, settings, scores, obstacles)  # check for input events

        distance_to_obstacle = game_func.calculate_distance_to_obstacle(main_character, obstacles, settings)
        nn_model_input = np.array([settings.object_velocity, distance_to_obstacle]).reshape(1, -1)

        nn_prediction = nn_model.predict(nn_model_input, verbose=0)[0]
        print("Prediction: ", nn_prediction)

        # jump if the nn predicted to do so or if the number of game loops is below 1000
        if nn_prediction[1] > nn_prediction[0] or loops < 1000:
            game_func.initiate_jump(main_character, jump_sound, settings, scores, obstacles)

        # makes sure to generate the obstacle/prize at appropriate intervals
        if obstacle_interval >= settings.obstacle_interval:
            # try to generate new obstacles
            if game_func.generate_object(coins, Coin, screen, settings, settings.prize_generation_probability):
                obstacle_interval = 0
            # try to generate a new prize
            else:
                for obstacle_class in obstacle_classes:
                    if game_func.generate_object(obstacles, obstacle_class, screen, settings,
                                                 settings.obstacle_generation_probability):
                        obstacle_interval = 0
                        break
        game_func.generate_object(clouds, Cloud, screen, settings, settings.cloud_generation_probability)

        # update the states of the sprites and the main character
        game_func.update_objects(obstacles, scores)
        game_func.update_objects(coins, scores)
        game_func.update_objects(clouds, scores)
        main_character.update()

        main_character.blit_sprite()
        main_character.advance_animation()
        scores.blit_scoreboards()

        game_func.check_collisions(main_character, obstacles, coins, win_sound, crash_sound, settings, scores)

        clock.tick(settings.fps)  # clock the game to the specific fps
        pygame.display.flip()  # refresh the screen
        settings.increase_difficulty()

        print(f"Obstacles: {len(scores.success)}; Game Loops: {loops}")

        # (re)train the NN model only when at least 10 data points collected every 500 loops of the game
        if len(scores.success) >= 10 and loops % 500 == 0:
            nn_model = neural_network.train_nn_model(nn_model, scores.velocities, scores.distances, scores.success)

        loops += 1
        obstacle_interval += 1


if __name__ == '__main__':
    run_game()
