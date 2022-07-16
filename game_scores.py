from game_func import calculate_distance_to_obstacle
import pygame.font


class GameScores:
    """ Represents the game scores and statistics """

    def __init__(self, settings, screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = settings

        # set up the initial jump data
        self.temp_velocity = None
        self.temp_distance = None
        self.velocities = []
        self.distances = []
        self.success = []

        # set up the scoreboard font and colour
        self.text_colour = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 25)

        # set up the initial scores
        self.max_score = 0
        self.set_default_scores()
        self.prepare_score()
        self.prepare_high_score()

    def set_default_scores(self):
        # self.num_objects_avoided = 0
        self.current_score = 0

    def collect_jump_data(self, settings, dino, obstacles):
        """ Collects the jump parameters at the very beginning of a jump """
        self.temp_velocity = settings.object_velocity
        self.temp_distance = calculate_distance_to_obstacle(dino, obstacles, settings)

    def save_jump_data(self, success):
        """ Saves the parameters of a jump together with the jump outcome (success/failure) """
        if self.temp_velocity and self.temp_distance:
            self.velocities.append(self.temp_velocity)
            self.distances.append(self.temp_distance)
        else:  # this is the case when there was no jump
            self.velocities.append(self.settings.object_velocity)
            self.distances.append(0)
        self.success.append(success)
        # rest the most recent jump data
        self.temp_velocity = None
        self.temp_distance = None

    def prepare_scores(self):
        """ Prepares all the game scores to display """
        self.prepare_score()
        self.update_max_score()
        self.prepare_high_score()

    def blit_scoreboards(self):
        """ Draws the game scores on the screen """
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

    def prepare_score(self):
        """ Prepares the current game score text """
        self.score_image = self._render_text_image("Score: ", self.current_score)
        # text image orientation
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prepare_high_score(self):
        """ Prepares the highest game score text """
        self.high_score_image = self._render_text_image("Highest Score: ", self.max_score)
        # text image orientation
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left + 20
        self.high_score_rect.top = 20

    def _render_text_image(self, title, stat):
        """ Renders text """
        msg = title + str(stat)
        return self.font.render(msg, True, self.text_colour)

    def update_max_score(self):
        """ Updates the highest game score in a game session """
        self.max_score = self.current_score if self.max_score < self.current_score else self.max_score
