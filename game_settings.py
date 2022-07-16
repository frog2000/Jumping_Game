import pygame
import os


class Settings:
    """ Main game settings """
    def __init__(self):

        # set the game's window size
        self.window_width = 900
        self.window_height = 400

        self.fps = 60  # set the maximum frames per second
        self.background = pygame.transform.scale(pygame.image.load_extended(os.path.join("images", "background.png")),
        (self.window_width, self.window_height))  # set the background image

        self.main_character_acceleration = 2
        self.animation_interval = self.fps/45  # character animation speed
        self.speed_up_factor = 1.0001  # how quickly the game speeds up

        self.set_main_character_velocity()
        self.set_objects_default_param()
        self.obstacle_generation_probability = 100
        self.prize_generation_probability = 500
        self.cloud_generation_probability = 300

    def set_main_character_velocity(self):
        self.main_character_jump_velocity = 30

    def set_objects_default_param(self):
        self.object_velocity = 8
        self.obstacle_interval = 40

    def increase_difficulty(self):
        self.object_velocity *= self.speed_up_factor
        self.obstacle_interval /= self.speed_up_factor

