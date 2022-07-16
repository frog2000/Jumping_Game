import pygame
import sys
from playsound import playsound  # version 1.2.2 works fine
import threading
import random
import time


def play_sound(sound_file_path):
    playsound(sound_file_path)


def check_events(main_character, jump_sound, settings, scores, obstacles):
    """ Checks for the user input events """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_UP, pygame.K_SPACE]:
                initiate_jump(main_character, jump_sound, settings, scores, obstacles)


def initiate_jump(main_character, jump_sound, settings, scores, obstacles):
    """ Makes the main character to initiate the jump """
    if not main_character.character_jumping:
        main_character.character_jumping = True
        scores.collect_jump_data(settings, main_character, obstacles)
        threading.Thread(target=play_sound, args=[jump_sound]).start()


def _check_if_event_happens(probability_factor):
    """ Check if an event that has a particular probability to happen, happens """
    if 0 == random.randint(0, int(probability_factor)):
        return True
    return False


def generate_object(objects, obj, screen, settings, probability_factor):
    """ Adds a new object to the game with a specified probability """
    if _check_if_event_happens(probability_factor):
        objects.add(obj(screen, settings))
        return True
    return False


def update_objects(objects, scores):
    """ Updates the object states """
    objects.update(objects, scores)
    for obj in objects:
        obj.blit_sprite()


def check_mask_collide(obj1, obj2):
    """ Checks for a mask collision between two objects """
    offset_x = obj2.rect.x - obj1.rect.x
    offset_y = obj2.rect.y - obj1.rect.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None


def check_collisions(main_character, obstacles, coins, win_sound, crash_sound, settings, scores):
    """ Checks for a collision between the main game character and other objects in the game """
    for obstacle in obstacles:
        if check_mask_collide(main_character, obstacle):
            threading.Thread(target=play_sound, args=[crash_sound]).start()
            main_character_crash(main_character, obstacles, coins, settings, scores)
            scores.set_default_scores()
            scores.save_jump_data(0)
            break

    for coin in coins:
        if check_mask_collide(main_character, coin):
            threading.Thread(target=play_sound, args=[win_sound]).start()
            coins.remove(coin)
            give_prize(scores)
            break


def give_prize(scores):
    """ Awards a special score prize """
    scores.current_score += 100
    scores.prepare_scores()
    

def main_character_crash(main_character, obstacles, coins, settings, scores):
    """ Simulates a crash of the main character and resets the game """
    main_character.reset_position()
    settings.set_objects_default_param()
    scores.set_default_scores()
    scores.prepare_scores()

    for obstacle in obstacles.copy():
        obstacles.remove(obstacle)
        del obstacle
    for coin in coins.copy():
        coins.remove(coin)
        del coin
    time.sleep(1)


def calculate_distance_to_obstacle(main_character, obstacles, settings):
    """ Finds the distance between the main character and the nearest obstacle """
    if obstacles.sprites():
        return obstacles.sprites()[0].rect.left - main_character.rect.right
    else:
        return settings.window_width
