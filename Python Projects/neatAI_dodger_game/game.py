import pygame
import random


# CONST VARIABLES ======================================================================================================
# WINDOW
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500

# FLOOR
FLOOR_WIDTH = 1000
FLOOR_HEIGHT = 100

# DODGER
DODGER_SPAWN_X = WINDOW_WIDTH / 8
DODGER_SPAWN_Y = WINDOW_HEIGHT - FLOOR_HEIGHT + 20
DODGER_ANIMATION_DELAY = 250

# OBSTACLE
OBSTACLE_SPAWN_X = WINDOW_WIDTH + 200
OBSTACLE_SPAWN_Y = WINDOW_HEIGHT - FLOOR_HEIGHT + 20
OBSTACLE_NUMBER = 3
# ======================================================================================================================


# CLASSES ==============================================================================================================
class Environment:
    def __init__(self, environment_sprite: str, x_start, y_start):
        self.environment_sprite = environment_sprite
        self.environment = pygame.image.load(self.environment_sprite).convert()

        self.x_start = x_start
        self.y_start = y_start

    def scroll(self, offset):
        for _i in range(0, 2):
            window.blit(self.environment, (self.environment.get_width() * _i + offset, self.y_start))
        if abs(offset) > self.environment.get_width():
            offset = 0
        offset -= 1

        return offset

    def draw(self):
        window.blit(self.environment, (self.x_start, self.y_start))


class Dodger:
    def __init__(self, x_start=DODGER_SPAWN_X, y_start=DODGER_SPAWN_Y):
        self.dodger_walk1_sprite = pygame.image.load("sprites/dodger/walk1.png").convert_alpha()
        self.dodger_walk2_sprite = pygame.image.load("sprites/dodger/walk2.png").convert_alpha()
        self.dodger_crouch1_sprite = pygame.image.load("sprites/dodger/crouch1.png").convert_alpha()
        self.dodger_crouch2_sprite = pygame.image.load("sprites/dodger/crouch2.png").convert_alpha()

        self.x_start = x_start
        self.y_start = y_start

        self.velocity = 0.0
        self.is_falling = False
        self.is_grounded = True
        self.is_crouching = False

        self.dodger = self.dodger_walk1_sprite.get_rect()
        self.dodger.midbottom = (x_start, y_start)

    def stand_up(self):
        if self.is_grounded and not self.is_falling:
            self.is_crouching = False

            self.dodger = self.dodger_walk1_sprite.get_rect()
            self.dodger.midbottom = (self.x_start, self.y_start)

    def crouch(self):
        if self.is_grounded and not self.is_falling:
            self.is_crouching = True

            self.dodger = self.dodger_crouch1_sprite.get_rect()
            self.dodger.midbottom = (self.x_start, self.y_start)

    def jump(self, velocity: float):
        if self.is_grounded and not self.is_crouching:
            self.velocity -= velocity
            self.is_falling = True
            self.is_grounded = False

    def gravity(self, gravity_force: float, gravity_force_cap: float):
        if self.is_falling:
            self.velocity += gravity_force

            if self.velocity >= gravity_force_cap:
                self.velocity = gravity_force_cap

            self.dodger.y += self.velocity

        if self.dodger.bottom >= self.y_start:
            self.dodger.bottom = self.y_start
            self.is_falling = False
            self.is_grounded = True
            self.velocity = 0

    def draw(self, old_tick, new_tick, _counter):

        if not self.is_crouching:
            sprite_list = [self.dodger_walk1_sprite, self.dodger_walk2_sprite]
        else:
            sprite_list = [self.dodger_crouch1_sprite, self.dodger_crouch2_sprite]

        if new_tick - old_tick >= DODGER_ANIMATION_DELAY:
            if _counter == 1:
                _counter = 0
            else:
                _counter += 1
            window.blit(sprite_list[_counter], self.dodger)
            old_tick = new_tick
        else:
            window.blit(sprite_list[_counter], self.dodger)

        return old_tick, _counter


class Obstacle:
    def __init__(self, obstacle_sprite: str, move_speed: int, x_start=OBSTACLE_SPAWN_X, y_start=OBSTACLE_SPAWN_Y,
                 rope_sprite: str = None):
        self.move_speed = move_speed

        self.x_start = x_start
        self.y_start = y_start

        self.passed_player = False

        self.rope_sprite = pygame.image.load(rope_sprite).convert_alpha() if rope_sprite else None
        self.obstacle_sprite = pygame.image.load(obstacle_sprite).convert_alpha()
        self.obstacle = self.obstacle_sprite.get_rect()
        self.obstacle.midbottom = (x_start, y_start)

    def move(self):
        self.obstacle.x -= self.move_speed

    def check_passed_player(self):
        if not self.passed_player and self.obstacle.right + 10 < DODGER_SPAWN_X:
            self.passed_player = True

    def check_for_collision(self, _player):
        return self.obstacle.colliderect(_player)

    def draw(self):
        window.blit(self.obstacle_sprite, self.obstacle)

        if self.rope_sprite:
            window.blit(self.rope_sprite, (self.obstacle.x, self.obstacle.y - self.rope_sprite.get_height() + 4))
# ======================================================================================================================


# FUNCTIONS ============================================================================================================
# Dodger
def spawn_dodger():
    _dodger = Dodger(DODGER_SPAWN_X, DODGER_SPAWN_Y)

    return _dodger


# Obstacle
def is_time_to_spawn_obstacle(old_tick, new_tick, _obstacle_list):
    if len(_obstacle_list) < OBSTACLE_NUMBER and new_tick - old_tick >= 2000:
        _obstacle_list.append(spawn_obstacle())
        old_tick = new_tick

    return old_tick, _obstacle_list


def spawn_obstacle():
    obstacle_types = [["sprites/obstacle/spiky_cube.png", 5, OBSTACLE_SPAWN_X, OBSTACLE_SPAWN_Y - 120,
                       "sprites/obstacle/rope_cube.png"],
                      ["sprites/obstacle/spiky_rectangle.png", 5, OBSTACLE_SPAWN_X, OBSTACLE_SPAWN_Y - 40,
                       "sprites/obstacle/rope_rectangle.png"],
                      ["sprites/obstacle/small_spiky_cube.png", 5, OBSTACLE_SPAWN_X, OBSTACLE_SPAWN_Y,
                       "sprites/obstacle/rope_small_spiky_cube.png"]]

    obstacle_weights = random.choice([0, 1, 2, 2])

    _obstacle = Obstacle(*obstacle_types[obstacle_weights])

    return _obstacle


# Score
def update_score(old_tick, new_tick, _score):
    if new_tick - old_tick >= 25:
        _score += 1
        old_tick = new_tick
    score_text = score_font.render(str(_score), True, (0, 0, 0))
    score_rect = score_text.get_rect()
    score_rect.topright = (980, 20)
    window.blit(score_text, score_rect)

    return old_tick, _score


# Init =================================================================================================================
pygame.init()
pygame.display.set_caption("Dodger")
clock = pygame.time.Clock()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Environment ==========================================================================================================
background = Environment("sprites/environment/background.png", 0, 0)
floor = Environment("sprites/environment/floor.png", 0, WINDOW_HEIGHT - FLOOR_HEIGHT)

# Score  ===============================================================================================================
score_font = pygame.font.Font(None, 30)


# Main =================================================================================================================
def main():
    # Environment
    background_offset = 0
    floor_offset = 0

    # Score
    score = 0
    old_score_tick = pygame.time.get_ticks()

    # Obstacle
    obstacles_list = [spawn_obstacle()]
    old_obstacle_tick = pygame.time.get_ticks()

    # Dodger
    dodger = spawn_dodger()
    old_dodger_tick = pygame.time.get_ticks()
    dodger_frame = 0

    # Game loop ========================================================================================================
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    dodger.jump(24)
                elif event.key == pygame.K_s:
                    dodger.crouch()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    dodger.stand_up()

        # Environment
        background_offset = background.scroll(background_offset)
        floor_offset = floor.scroll(floor_offset)
        # ==============================================================================================================

        # Score
        new_score_tick = pygame.time.get_ticks()
        old_score_tick, score = update_score(old_score_tick, new_score_tick, score)
        # ==============================================================================================================

        # Dodger
        dodger.gravity(1.5, 10)

        new_dodger_tick = pygame.time.get_ticks()
        old_dodger_tick, dodger_frame = dodger.draw(old_dodger_tick,
                                                    new_dodger_tick, dodger_frame)
        # ==============================================================================================================

        # Obstacle
        new_obstacle_tick = pygame.time.get_ticks()
        old_obstacle_tick, obstacles_list = is_time_to_spawn_obstacle(old_obstacle_tick, new_obstacle_tick,
                                                                      obstacles_list)

        for obstacle in reversed(obstacles_list):
            if obstacle.obstacle.x <= -200:
                obstacles_list.remove(obstacle)
                continue

            obstacle.draw()
            obstacle.move()

            # Needed only for training NEAT
            # obstacle.check_passed_player()

            if obstacle.check_for_collision(dodger.dodger):
                exit(0)
        # ==============================================================================================================

        # Pygame stuff
        clock.tick(60)
        pygame.display.update()
        # ==============================================================================================================


if __name__ == '__main__':
    main()
