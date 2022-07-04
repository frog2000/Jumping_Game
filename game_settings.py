import pygame
import os


class Settings:
    def __init__(self):
        self.window_width = 900
        self.window_height = 400
        self.fps = 60
        # self.background = (255, 255, 255)
        self.background = pygame.transform.scale(pygame.image.load_extended(os.path.join("images", "background.png")),
        (self.window_width, self.window_height))

        self.dino_acceleration = 2
        self.animation_interval = self.fps/45
        self.speed_up_factor = 1.0001

        self.set_dino_velocity()
        self.set_objects_default_param()
        self.obstacle_generation_probability = 100
        self.prize_generation_probability = 500
        self.cloud_generation_probability = 300

    def set_dino_velocity(self):
        self.dino_jump_velocity = 30

    def set_objects_default_param(self):
        self.object_velocity = 8
        self.obstacle_interval = 40

    def increase_difficulty(self):
        self.object_velocity *= self.speed_up_factor
        self.obstacle_interval /= self.speed_up_factor

