import random

class Game:
    def __init__(self, window):
        self.window = window
        self.distance = 0
        self.energy = 100
        self.lane = 1
        self.speed = 8
        self.is_game_over = False
        self.obstacles = []
        self.energy_drinks = []
        self.max_lanes = 3
        self.max_distance = 100
        self.prev=None
        self.lanes=[65, 400, 700]

    def get_stats(self):
        return self.energy, self.distance, self.obstacles, self.energy_drinks, self.lane

    def move_character(self):
        if self.is_game_over:
            return
        self.energy -= 1
        self.distance += 1
        if self.energy <= 0:
            self.is_game_over = True
        self.check_for_obstacles()
        self.check_for_energy_drinks()
        self.remove_out_of_bounds_items()

    def check_for_obstacles(self):
        if random.random() < 0.3:
            self.spawn_obstacle()
        if any(obstacle['lane'] == self.lane for obstacle in self.obstacles):
            self.energy -= 20
            self.obstacles = [o for o in self.obstacles if o['lane'] != self.lane]

    def check_for_energy_drinks(self):
        if random.random() < 0.2:
            self.spawn_energy_drink()
        if any(drink['lane'] == self.lane for drink in self.energy_drinks):
            self.energy += 20
            self.energy_drinks = [d for d in self.energy_drinks if d['lane'] != self.lane]

    def spawn_obstacle(self):
        lane = random.randint(0, 2)
        self.obstacles.append({'lane': lane, 'position': self.distance + random.randint(2, 5)})

    def spawn_energy_drink(self):
        lane = random.randint(0, 2)
        self.energy_drinks.append({'lane': lane, 'position': self.distance + random.randint(2, 5)})

    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            return f"Moved to lane {self.lane}"
        return "Already in the leftmost lane."

    def move_right(self):
        if self.lane < self.max_lanes - 1:
            self.lane += 1
            return f"Moved to lane {self.lane}"
        return "Already in the rightmost lane."

    def remove_out_of_bounds_items(self):
        self.obstacles = [o for o in self.obstacles if o['position'] > self.distance]
        self.energy_drinks = [d for d in self.energy_drinks if d['position'] > self.distance]

    def draw_obstacles(self, canvas):
        for obstacle in self.obstacles:
            if obstacle["lane"]==0:
                x=65
                y=565
            elif obstacle["lane"]==1:
                    x=400
                    y=530

            elif obstacle["lane"]==2:
                    x=700
                    y=530
            canvas.create_rectangle(x, y,
                                        x+20, y+20,
                                        fill="red")

    def draw_energy_drinks(self, canvas):
        for drink in self.energy_drinks:
            if drink['position'] >= self.distance:
                canvas.create_oval(drink['position'] * 8, 100 + drink['lane'] * 100,
                                   drink['position'] * 8 + 20, 120 + drink['lane'] * 100,
                                   fill="blue")

    def draw_character(self, canvas):
        if self.prev is not None:
            canvas.delete(self.prev)
        # Draw the character as a green rectangle in the current lane
        self.prev=canvas.create_rectangle(self.lanes[self.lane], 50, self.lanes[self.lane]+20, 70, fill="green")