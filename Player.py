import os
import random
import pygame as pg

from Rectangle import Rectangle
import Var

blue_img = pg.image.load(os.path.join('Assets', 'blue_square.png'))

class Player(Rectangle):
    """ Creates a player """
    def __init__(self, x, y, width, height, WIN):
        super().__init__(x, y, width, height, WIN)
        self.img = pg.transform.scale(blue_img, (self.width, self.height))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.jump_count = 10
        self.vert_vel = 0
        self.on_ground = False

    def update_player(self):
        """ Updates the position of the player and updates player movement """
        self.x, self.y = self.rect.x, self.rect.y
        self.handle_movement()

    def draw_players(self, players, enemies):
        """
        Draws multiple players
        Draws a border around each player and a line to the midtop of enemy
        """
        for player in players:
            player.draw()
            pg.draw.rect(self.WIN, player.color, (player.x,
                         player.y, player.width, player.height), 3)
            for enemy in enemies:
                pg.draw.line(self.WIN, player.color, (player.x + 50, player.y + 12), enemy.rect.topleft, 2)

    def jump(self):
        """ Tells player to jump """
        if self.on_ground:
            self.vert_vel = -13

    def handle_movement(self):
        """ Handles player jumping and stops player from falling through floor """
        self.rect.y += self.vert_vel

        if self.rect.bottom == 475:
            self.on_ground = True
        else:
            self.on_ground = False

        if self.on_ground:
            self.vert_vel = 0
        else:
            self.vert_vel += 0.5

        if self.vert_vel >= 50:
            self.vert_vel = 50

    def get_mask(self):
        """ Gets the mask of the player """
        return pg.mask.from_surface(self.img)
