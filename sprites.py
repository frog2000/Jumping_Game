import pygame
from pygame.sprite import Sprite
import os
import random
from abc import ABC


cactus_image = pygame.image.load_extended(os.path.join("images", "cactus.png"))
rock_image = pygame.image.load_extended(os.path.join("images", "rock.png"))
coin_image = pygame.image.load_extended(os.path.join("images", "coin.png"))
cloud_image = pygame.image.load_extended(os.path.join("images", "cloud.png"))
path_main_character_images = os.path.join("images", "girl")
main_character_images = [pygame.image.load_extended(os.path.join(path_main_character_images, image))
                         for image in os.listdir(path_main_character_images) if
                         os.path.isfile(os.path.join(path_main_character_images, image))]


class MainCharacter:
    """ The class representing the main character of the jumping game """

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()

        # set up the character image, mask and rectangle
        self.character_images = main_character_images
        self.character_image = self.character_images[0]
        self.mask = pygame.mask.from_surface(self.character_image)
        self.rect = self.character_image.get_rect()

        # set up the character position
        self.rect.centerx = self.screen_rect.left + 60
        self.reset_position()
        self.bottom = float(self.rect.bottom)

        # set up the initial jumping state
        self.character_jumping = False
        self.jump_time = 1

        # set up the initial character animation parameters
        self.current_animation_time = 0
        self.current_image = 0

    def update(self):
        """ Updates the main character position on the y-axis - so simulates jumping """
        if self.character_jumping:
            # check if moving up
            if self.settings.main_character_jump_velocity > 0:
                self.bottom -= self.settings.main_character_jump_velocity
                self.settings.main_character_jump_velocity -= self.settings.main_character_acceleration * self.jump_time**2
                # check if the character reached the jump apex
                if self.settings.main_character_jump_velocity <= 0:
                    self.jump_time = 1
            else:  # moving down
                self.bottom -= self.settings.main_character_jump_velocity
                self.settings.main_character_jump_velocity -= self.settings.main_character_acceleration * self.jump_time**2
                if self.bottom >= self.screen_rect.bottom:
                    # reset the jump settings and parameters when the character reached the ground
                    self.reset_position()
                    self.jump_time = 1
                    self.character_jumping = False
                    self.settings.set_main_character_velocity()

        self.rect.bottom = self.bottom

    def blit_sprite(self):
        """ Draws the main character image """
        self.screen.blit(self.character_image, self.rect)

    def reset_position(self):
        """ Resets the main character image position to the bottom of the window """
        self.rect.bottom = self.screen_rect.bottom

    def advance_animation(self):
        """ Progresses the main character animation at an appropriate pace """
        self.current_animation_time += 1
        if self.current_animation_time >= self.settings.animation_interval:
            # a new character animation image is loaded at a specific interval
            self._next_image()
            self.current_animation_time = 0  # reset the animation interval time

    def _next_image(self):
        """ Loads a new character animation image """
        if self.current_image >= len(self.character_images) - 1:
            self.current_image = 0  # start with the first image if the animation went through all the images
        else:
            self.current_image += 1
        self.character_image = self.character_images[self.current_image]
        self.mask = pygame.mask.from_surface(self.character_image)


class GameSprite(ABC, Sprite):
    """ The 'abstract' class representing the game sprites (all but the main character) """

    def __init__(self, screen, settings, image):
        super().__init__()
        self.screen = screen
        self.settings = settings

        # set up the sprite image, mask and rectangle
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # set up the sprite position on the screen
        self.rect.centerx = self.screen_rect.right + self.rect.width
        self.rect.bottom = self.screen_rect.bottom + 5
        self.centerx = float(self.rect.centerx)

    def blit_sprite(self):
        """ Draws the sprite image on the screen """
        self.screen.blit(self.image, self.rect)

    def update(self, group, scores):
        """ Updates the sprite position on the x-axis """
        self.centerx -= self.settings.object_velocity
        self.rect.centerx = self.centerx

        # check if the sprite instance left the screen
        if self.rect.right <= 0:
            group.remove(self)  # remove from the sprite group
            scores.current_score += 10
            scores.prepare_scores()
            scores.save_jump_data(1)
            del self


class Cactus(GameSprite):
    """ Class representing an obstacle - cactus """
    def __init__(self, screen, settings):
        self.image = cactus_image
        super().__init__(screen, settings, self.image)


class Rock(GameSprite):
    """ Class representing an obstacle - rock """
    def __init__(self, screen, settings):
        self.image = rock_image
        super().__init__(screen, settings, self.image)
        self.rect.bottom = self.screen_rect.bottom + 25


class Coin(GameSprite):
    """ Class representing a coin """
    def __init__(self, screen, settings):
        self.image = coin_image
        super().__init__(screen, settings, self.image)
        self.rect.bottom = self.screen_rect.bottom - 10

    def update(self, group, scores):
        """ Allows for the alien movement on the x-axis """
        self.centerx -= self.settings.object_velocity
        self.rect.centerx = self.centerx

        if self.rect.right <= 0:
            group.remove(self)
            scores.current_score += 10
            del self


class Cloud(GameSprite):
    """ Class representing a cloud """
    def __init__(self, screen, settings):
        self.image = cloud_image
        super().__init__(screen, settings, self.image)
        # place the cloud at a random height
        self.rect.bottom = random.randint(70, int(0.4*self.screen_rect.bottom))
        self.cloud_velocity = self.settings.object_velocity*(random.randint(30, 50)/100)

    def update(self, group, scores=None):
        """ Updates the sprite position on the x-axis """
        self.centerx -= self.cloud_velocity
        self.rect.centerx = self.centerx

        # check if the sprite instance left the screen
        if self.rect.right <= 0:
            group.remove(self)
            del self
