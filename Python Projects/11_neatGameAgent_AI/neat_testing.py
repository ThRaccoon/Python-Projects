import neat
import pygame
import pickle
import os.path
import game as gm


# Testing ==============================================================================================================
def test_genome(genome, config):
    # Environment
    background_offset = 0
    floor_offset = 0

    # Score
    score = 0
    old_score_tick = pygame.time.get_ticks()

    # Obstacle
    obstacles_list = [gm.spawn_obstacle()]
    old_obstacle_tick = pygame.time.get_ticks()

    # Dodger
    dodger = gm.spawn_dodger()
    old_dodger_tick = pygame.time.get_ticks()
    dodger_frame = 0

    # Neat
    nn = neat.nn.FeedForwardNetwork.create(genome, config)

    # Game loop ========================================================================================================
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        # Environment
        background_offset = gm.background.scroll(background_offset)
        floor_offset = gm.floor.scroll(floor_offset)
        # ==============================================================================================================

        # Score
        new_score_tick = pygame.time.get_ticks()
        old_score_tick, score = gm.update_score(old_score_tick, new_score_tick, score)
        # ==============================================================================================================

        # Dodger
        dodger.gravity(1.5, 10)

        new_dodger_tick = pygame.time.get_ticks()
        old_dodger_tick, dodger_frame = dodger.draw(old_dodger_tick,
                                                    new_dodger_tick, dodger_frame)
        # =============================================================================================================

        # Obstacle
        new_obstacle_tick = pygame.time.get_ticks()
        old_obstacle_tick, obstacles_list = gm.is_time_to_spawn_obstacle(old_obstacle_tick, new_obstacle_tick,
                                                                         obstacles_list)

        for obstacle in reversed(obstacles_list):
            if obstacle.obstacle.x <= -200:
                obstacles_list.remove(obstacle)
                continue

            obstacle.draw()
            obstacle.move()
            obstacle.check_passed_player()

            if obstacle.check_for_collision(dodger.dodger):
                exit(0)
        # ==============================================================================================================

        # NEAT
        # Get the closest obstacle
        closest_obstacle = next((obs for obs in obstacles_list if not obs.passed_player), None)

        # NN decision making
        distance_left = closest_obstacle.obstacle.left - dodger.dodger.right
        distance_right = (closest_obstacle.obstacle.right + 10) - dodger.dodger.left
        output = nn.activate([
            distance_left,
            distance_right,
            dodger.dodger.y,
            dodger.is_grounded,
            dodger.is_crouching,
            closest_obstacle.obstacle.y
            ])

        decision = output.index(max(output))

        if decision == 0:
            if dodger.is_crouching:
                dodger.stand_up()
            pass
        elif decision == 1:
            if dodger.is_crouching:
                dodger.stand_up()
            dodger.jump(24)
        else:
            dodger.crouch()
        # ==============================================================================================================

        # Pygame stuff
        gm.clock.tick(60)
        pygame.display.update()
        # ==============================================================================================================


def run(_config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        _config_path
    )

    with open("best_genome.pkl", "rb") as file:
        best_genome = pickle.load(file)

    test_genome(best_genome, config)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
