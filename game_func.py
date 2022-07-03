import pygame
import sys
from playsound import playsound  # version 1.2.2 works fine
import threading
import random
import time


def play_sound(sound_file_path):
    playsound(sound_file_path)


def check_events(dino, jump_sound):
    """ Checks for input events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_SPACE]:
                dino.jump()
                threading.Thread(target=play_sound, args=[jump_sound]).start()


def _check_if_event_happens(probability_factor):
    """ Check if an event that has a particular probability to happen, happens """
    if 0 == random.randint(0, int(probability_factor)):
        return True
    return False


def generate_object(objects, obj, screen, settings, probability_factor):
    if _check_if_event_happens(probability_factor):
        objects.add(obj(screen, settings))
        return True
    return False


def update_objects(objects):
    objects.update(objects)
    for obj in objects:
        obj.blit_sprite()


def check_mask_collide(obj1, obj2):
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def check_collisions(dino, obstacles, coins, win_sound, crash_sound, settings):
    for obstacle in obstacles:
        if check_mask_collide(dino, obstacle):
            threading.Thread(target=play_sound, args=[crash_sound]).start()
            dino_crash(dino, obstacles, coins, settings)
            break

    for coin in coins:
        if check_mask_collide(dino, coin):
            threading.Thread(target=play_sound, args=[win_sound]).start()
            coins.remove(coin)
            give_reward()
            break


def dino_crash(dino, obstacles, coins, settings):
    dino.reset_position()
    settings.set_objects_default_param()

    for obstacle in obstacles.copy():
        obstacles.remove(obstacle)
        del obstacle
    for coin in coins.copy():
        coins.remove(coin)
        del coin
    time.sleep(1)


def give_reward():
    pass