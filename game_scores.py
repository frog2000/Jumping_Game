from game_func import calculate_distance_to_obstacle

class GameScores:

    def __init__(self, settings):
        self.settings = settings
        self.max_score = 0
        self.velocities = []
        self.distances = []
        self.success = []

        self.temp_velocity = None
        self.temp_distance = None

        self.set_default_scores()

    def set_default_scores(self):
        self.num_objects_avoided = 0
        self.current_score = 0

    def collect_jump_data(self, settings, dino, obstacles):
        self.temp_velocity = settings.object_velocity
        self.temp_distance = calculate_distance_to_obstacle(dino, obstacles, settings)

    def save_jump_data(self, success):
        if self.temp_velocity and self.temp_distance:
            self.velocities.append(self.temp_velocity)
            self.distances.append(self.temp_distance)
        else:
            self.velocities.append(self.settings.object_velocity)
            self.distances.append(0)
        self.temp_velocity = None
        self.temp_distance = None
        self.success.append(success)
