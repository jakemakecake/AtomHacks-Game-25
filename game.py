import random

class Game:
    def __init__(self, window):
        self.window = window
        self.distance = 0
        self.energy = 100  # Energy starts at 100%
        self.lane = 1  # Start in the middle lane
        self.speed = 8  # Run 8 pixels per frame (or per second)
        self.is_game_over = False  # Game Over state
        self.obstacles = []
        self.energy_drinks = []

        # Some additional setup variables
        self.max_lanes = 3  # We have 3 lanes: 0, 1, 2
        self.max_distance = 100  # Arbitrary large distance to trigger Game Over

        # Timer for energy consumption
        self.last_energy_time = 0

    def get_stats(self):
        """Return the current status: energy, distance, obstacles, energy_drinks, lane"""
        return self.energy, self.distance, self.obstacles, self.energy_drinks, self.lane

    def move_character(self):
        """Move the character automatically and handle game mechanics."""
        if self.is_game_over:
            return

        # Decrease energy as the player runs
        self.energy -= 1  # Decrease energy per second

        # Update the game distance
        self.distance += 1  # Increase distance by 1 meter

        # Check if energy runs out
        if self.energy <= 0:
            self.is_game_over = True

        # Simulate obstacles and energy drinks
        self.check_for_obstacles()
        self.check_for_energy_drinks()

        # Remove obstacles and energy drinks that have passed
        self.remove_out_of_bounds_items()

    def check_for_obstacles(self):
        """Simulate obstacles spawning and handle collision."""
        if random.random() < 0.3:  # 30% chance of an obstacle spawning
            self.spawn_obstacle()

        # Check if any obstacles hit the character
        if any(obstacle['lane'] == self.lane for obstacle in self.obstacles):
            self.energy -= 20  # Decrease energy by 20 if you hit an obstacle
            self.obstacles = [obstacle for obstacle in self.obstacles if obstacle['lane'] != self.lane]

    def check_for_energy_drinks(self):
        """Simulate energy drinks spawning and handle collection."""
        if random.random() < 0.2:  # 20% chance of an energy drink spawning
            self.spawn_energy_drink()

        # If character is in a lane with an energy drink, collect it
        if any(energy_drink['lane'] == self.lane for energy_drink in self.energy_drinks):
            self.energy += 20  # Increase energy by 20 if you collect an energy drink
            self.energy_drinks = [energy_drink for energy_drink in self.energy_drinks if energy_drink['lane'] != self.lane]

    def spawn_obstacle(self):
        """Spawn an obstacle in a random lane."""
        lane = random.randint(0, 2)  # Random lane 0, 1, or 2
        self.obstacles.append({'lane': lane, 'position': self.distance + random.randint(2, 5)})

    def spawn_energy_drink(self):
        """Spawn an energy drink in a random lane."""
        lane = random.randint(0, 2)  # Random lane 0, 1, or 2
        self.energy_drinks.append({'lane': lane, 'position': self.distance + random.randint(2, 5)})

    def move_left(self):
        """Move the character left to lane 0."""
        if self.lane > 0:
            self.lane -= 1
            return f"Moved to lane {self.lane}"
        return "Already in the leftmost lane."

    def move_right(self):
        """Move the character right to lane 2."""
        if self.lane < self.max_lanes - 1:
            self.lane += 1
            return f"Moved to lane {self.lane}"
        return "Already in the rightmost lane."

    def remove_out_of_bounds_items(self):
        """Remove obstacles and energy drinks that have passed."""
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle['position'] > self.distance]
        self.energy_drinks = [energy_drink for energy_drink in self.energy_drinks if energy_drink['position'] > self.distance]



