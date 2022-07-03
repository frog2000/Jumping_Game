import pygame
from pygame.sprite import Sprite
import os
import random


cactus_image = pygame.image.load_extended(os.path.join("images", "cactus.png"))
rock_image = pygame.image.load_extended(os.path.join("images", "rock.png"))
coin_image = pygame.image.load_extended(os.path.join("images", "coin.png"))
cloud_image = pygame.image.load_extended(os.path.join("images", "cloud.png"))
path_main_character_images = os.path.join("images", "girl")
main_character_images = [pygame.image.load_extended(os.path.join(path_main_character_images, image))
                         for image in os.listdir(path_main_character_images) if
                         os.path.isfile(os.path.join(path_main_character_images, image))]

class Dino:

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.screen_rect = screen.get_rect()

        # set up the ship image and the rectangle

        # self.dino_animation = SpriteStripAnim('images/dino_running.png', (0, 0, 68, 64), 3, None, True, frames)
        # images = ["run1.png", "run2.png", "run3.png", "run4.png"]
        self.dino_images = main_character_images
        print(main_character_images)
        # self.dino_image = self.dino_animation.next()
        self.dino_image = self.dino_images[0]
        self.mask = pygame.mask.from_surface(self.dino_image)

        self.rect = self.dino_image.get_rect()

        # set up the ship position
        self.rect.centerx = self.screen_rect.left + 60
        self.rect.bottom = self.screen_rect.bottom
        self.bottom = float(self.rect.bottom)

        self.dino_jumping = False
        self.jump_time = 1
        self.current_animation_time = 0
        self.current_image = 0

    def update(self):
        """ Allows for the ship movement in two dimensions"""
        if self.dino_jumping:
            if self.settings.dino_jump_velocity > 0:
                self.bottom -= self.settings.dino_jump_velocity
                self.settings.dino_jump_velocity -= self.settings.dino_acceleration * self.jump_time**2
                if self.settings.dino_jump_velocity <= 0:
                    self.jump_time = 1
            else:
                self.bottom -= self.settings.dino_jump_velocity
                self.settings.dino_jump_velocity -= self.settings.dino_acceleration * self.jump_time**2
                if self.bottom >= self.screen_rect.bottom:
                    self.bottom = self.screen_rect.bottom
                    self.jump_time = 1
                    self.dino_jumping = False
                    self.settings.set_dino_velocity()

        self.rect.bottom = self.bottom

    def blit_sprite(self):
        """ Draws the ship image """
        self.screen.blit(self.dino_image, self.rect)

    def reset_position(self):
        """ Places the ship image in the middle of x-axis near the bottom of the screen """
        self.rect.centery = self.screen_rect.bottom - 40

    def advance_animation(self):
        self.current_animation_time += 1
        if self.current_animation_time >= self.settings.animation_interval:
            self._next_image()
            self.current_animation_time = 0

    # def jump(self):
    #     if not self.dino_jumping:
    #         self.dino_jumping = True

    def _next_image(self):
        if self.current_image >= len(self.dino_images) - 1:
            self.current_image = 0
        else:
            self.current_image += 1
        self.dino_image = self.dino_images[self.current_image]
        self.mask = pygame.mask.from_surface(self.dino_image)


class Cactus(Sprite):
    def __init__(self, screen, settings):
        super().__init__()

        self.screen = screen
        self.settings = settings
        self.image = cactus_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.right + self.rect.width
        self.rect.bottom = self.screen_rect.bottom + 5
        self.centerx = float(self.rect.centerx)

    def blit_sprite(self):
        """ Draws the ship image """
        self.screen.blit(self.image, self.rect)

    def update(self, group, scores):
        """ Allows for the alien movement on the x-axis """
        self.centerx -= self.settings.object_velocity
        self.rect.centerx = self.centerx

        if self.rect.right <= 0:
            group.remove(self)
            scores.current_score += 10
            scores.prepare_scores()
            scores.save_jump_data(1)
            del self


class Rock(Cactus):
    def __init__(self, screen, settings):
        super().__init__(screen, settings)
        self.image = rock_image
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen_rect.bottom + 25


class Coin(Cactus):
    def __init__(self, screen, settings):
        super().__init__(screen, settings)
        self.image = coin_image
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen_rect.bottom - 10

    def update(self, group, scores):
        """ Allows for the alien movement on the x-axis """
        self.centerx -= self.settings.object_velocity
        self.rect.centerx = self.centerx

        if self.rect.right <= 0:
            group.remove(self)
            scores.current_score += 10
            del self


class Cloud(Cactus):
    def __init__(self, screen, settings):
        super().__init__(screen, settings)
        self.image = cloud_image
        self.rect = self.image.get_rect()
        self.rect.bottom = random.randint(70, int(0.4*self.screen_rect.bottom))
        self.cloud_velocity = self.settings.object_velocity*(random.randint(30, 50)/100)

    def update(self, group, scores=None):
        """ Allows for the alien movement on the x-axis """
        self.centerx -= self.cloud_velocity
        self.rect.centerx = self.centerx

        if self.rect.right <= 0:
            group.remove(self)
            del self
