import neat
import pygame
import pickle
import os.path
import game as gm


# Training =============================================================================================================
def eval_genomes(genomes, config):
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
    dodgers_list = []
    dodger = gm.spawn_dodger()
    old_dodger_tick = pygame.time.get_ticks()
    dodger_frame = 0

    # Neat
    genomes_list = []
    nn_list = []
    old_neat_tick = pygame.time.get_ticks()

    for genome_id, genome in genomes:
        dodgers_list.append(gm.spawn_dodger())
        genomes_list.append(genome)
        nn = neat.nn.FeedForwardNetwork.create(genome, config)
        nn_list.append(nn)
        genome.fitness = 0

    # Game loop ========================================================================================================
    while len(dodgers_list) > 0:
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
        for dodger in dodgers_list:
            old_dodger_tick, dodger_frame = dodger.draw(old_dodger_tick,
                                                        new_dodger_tick, dodger_frame)
        # ==============================================================================================================

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

            # This way of collision checking is made for only 1 dodger
            # if obstacle.check_for_collision(dodger.dodger):
            # exit(0)
        # ==============================================================================================================

        # NEAT
        # Check for collision
        for i in reversed(range(len(dodgers_list))):
            dodger = dodgers_list[i]
            for obstacle in obstacles_list:
                if dodger.dodger.colliderect(obstacle.obstacle):
                    genomes_list[i].fitness -= 250
                    dodgers_list.pop(i)
                    genomes_list.pop(i)
                    nn_list.pop(i)
                    break

        # Get the closest obstacle
        closest_obstacle = next((obs for obs in obstacles_list if not obs.passed_player), None)

        # NN decision making
        for i, dodger in enumerate(dodgers_list):
            distance_left = closest_obstacle.obstacle.left - dodger.dodger.right
            distance_right = (closest_obstacle.obstacle.right + 10) - dodger.dodger.left
            output = nn_list[i].activate([
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

                if distance_left > 20:
                    genomes_list[i].fitness -= 10
                elif 10 <= distance_left < 20:
                    genomes_list[i].fitness += 5
                elif 0 < distance_left < 10:
                    genomes_list[i].fitness += 10
                else:
                    genomes_list[i].fitness -= 5

                if closest_obstacle.obstacle.bottom <= 320:
                    genomes_list[i].fitness -= 15

                if dodger.is_crouching:
                    dodger.stand_up()
                dodger.jump(24)
            else:
                if distance_left > 20:
                    genomes_list[i].fitness -= 10
                elif 10 <= distance_left < 20:
                    genomes_list[i].fitness += 5
                elif 0 < distance_left < 10:
                    genomes_list[i].fitness += 10
                else:
                    genomes_list[i].fitness -= 5

                if closest_obstacle.obstacle.bottom <= 320:
                    genomes_list[i].fitness -= 15

                dodger.crouch()

        new_neat_tick = pygame.time.get_ticks()
        if new_neat_tick - old_neat_tick >= 200:
            if len(dodgers_list) > 0:
                for i in range(len(dodgers_list)):
                    genomes_list[i].fitness += 1
                    old_neat_tick = new_neat_tick

        if score == 5000:
            print("Score of 10000 reached!")
            with open("best_genome.pkl", "wb") as file:
                pickle.dump(genomes_list[0], file)
                print("The best genome was saved!")
            break
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

    pop = neat.Population(config)
    pop.run(eval_genomes, 500)
    print("Here")


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
