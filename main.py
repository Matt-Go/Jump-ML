import os
import neat
import visualize
import math
import random as rand
import pygame as pg

import Player, Enemy
import Var

os.environ["PATH"] += os.pathsep + 'D:/Graphviz/bin'

pg.init()
pg.font.init()

pg.display.set_caption("Jump ML")

clock = pg.time.Clock()

WIN = pg.display.set_mode((Var.SCREEN_WIDTH, Var.SCREEN_HEIGHT))

FONT = pg.font.SysFont("comicsans", 40)

player = Player.Player(100, 425, 50, 50, WIN)
enemy = Enemy.Enemy(Var.SCREEN_WIDTH, 400, 50, 75, WIN)

def draw_window(score, max_score, players, enemies):
    """ Draws all the objects and text on screen """
    WIN.fill(Var.WHITE)

    # GROUND #
    pg.draw.rect(WIN, Var.BLACK, (0, 475, Var.SCREEN_WIDTH, 600))

    player.draw_players(players, enemies)
    enemy.draw_mult(enemies)

    score_text = FONT.render("Score: " + str(score), 1, Var.BLACK)
    max_score_text = FONT.render("Max Score: " + str(max_score), 1, Var.BLACK)

    WIN.blit(score_text, (10, 10))
    WIN.blit(max_score_text, (10, 40))

def handle_collision(players, enemies):
    """ 
    Checks to see if a player collides with an enemy
    Decreases player fitness if collision occurs
    """
    for enemy in enemies:
        for i, player in enumerate(players):
            if enemy.check_collision(player, enemy):
                ge[i].fitness -= 3
                players.pop(i)
                nets.pop(i)
                ge.pop(i)

def stats(players, ge):
    """ Displays how many players are alive and what the current generation is """
    alive_text = FONT.render(f'Players Alive:  {str(len(players))}', True, (0, 0, 0))
    gen_text = FONT.render(f'Generation:  {p.generation+1}', True, (0, 0, 0))
    WIN.blit(alive_text, (Var.SCREEN_WIDTH//2, 10))
    WIN.blit(gen_text, (Var.SCREEN_WIDTH//2, 40))


def distance(pos_a, pos_b):
    """ Calculates the distance between two objects """
    dx = pos_a[0] - pos_b[0]
    dy = pos_a[1] - pos_b[1]
    return math.sqrt(dx**2 + dy**2)

max_score = 0

def main(genomes, config):
    """ Handles the operation of the player learning to jump over the enemy """
    global players, enemies, ge, nets, max_score, score

    player = Player.Player(100, 425, 50, 50, WIN)
    enemy = Enemy.Enemy(Var.SCREEN_WIDTH, 400, 50, 75, WIN)

    nets = []
    ge = []
    players = []
    enemies = []

    for g_id, g in genomes:
        players.append(Player.Player(100, 425, 50, 50, WIN))
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        ge.append(g)
        g.fitness = 0

    score = 0

    running = True
    while running:
        clock.tick(75)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()

        for i, player in enumerate(players):
            player.update_player()
            for enemy in enemies:
                output = nets[i].activate(
                    (
                        player.y,
                        distance((player.x, player.y), enemy.rect.midtop)
                    )
                )
                if output[0] > 0.5:
                    player.jump()

        # Spawns an enemy when there are no enemies on screen
        if len(enemies) == 0:
            enemies.append(enemy)

        # Sets the max score
        if score > max_score:
                max_score = score

        # Moves to next generation when there are no players left
        if len(players) == 0:
            break

        draw_window(score, max_score, players, enemies)

        enemy.move_enemies(enemies)

        score = enemy.out_enemy(enemies, score, ge)[0]
        ge = enemy.out_enemy(enemies, score, ge)[1]

        handle_collision(players, enemies)
        
        stats(players, ge)

        pg.display.update()

def run(config_path):
    """ 
    Sets up NEAT and displays statistics
    Creates visualizations after last generation
    """
    global p
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    p = neat.Population(config)
    stats = neat.StatisticsReporter()
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print('\nBest genome:\n{!s}'.format(winner))

    node_names = {-1:'Player y-value', -2: 'Player distance from enemy', 0:'Jump'}
    visualize.draw_net(config, winner, True, node_names=node_names)
    visualize.plot_stats(stats, ylog=False, view=True)
    visualize.plot_species(stats, view=True)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-neat")
    run(config_path)
