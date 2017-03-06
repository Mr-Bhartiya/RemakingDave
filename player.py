"""
player.py
====

This file handles all the player creation and other aspects of the player like what action to assign,
what are it's current coordinates, etc.

This file does not run on it's own, run binder.py to play the game.

"""

import pygame
import os
from itertools import cycle

import binder

__author__ = "Roshan Rakesh, Shubham Jain, Rhitik Bhatt, Shubham Sharma"
__credits__ = ["Roshan Rakesh", "Shubham Jain", "Rhitik Bhatt", "Shubham Sharma"]
__license__ = "MIT"
__version__ = "Beta-0.0"
__maintainer__ = "Rhitik Bhatt"
__email__ = "bhattrhitik95-at-gmail-dot-com"
__status__ = "Beta"

# These constants will keep track of center of a sprite and the height and WIDTH of a sprite
CENTER = 22.5, 22.5
WIDTH_SPRITE, HEIGHT_SPRITE = 45, 45
FINAL_SIZE_X, FINAL_SIZE_Y = 180, 180
walking_action = ['walk-1','walk-2', 'walk-3', 'walk-4']
cowboy_sprite = pygame.image.load(os.path.abspath('assets/cowboy.png'))

# This will help us cycle over the elements of walking_action
actions = cycle(walking_action)

# The actions in Cowboy2.png has the mentioned action at specified coordinates
# syntax
# 'action' : (x-coordinate, y-coordinate)

ACTIONS = {
    'gun-stand': (0, 0),
    'gun-shoot': (5, 0),
    'shoot-stars': (6, 0),
    'walk-gun-1': (0, 1),
    'walk-gun-2': (1, 1),
    'walk-gun-3': (2, 1),
    'walk-gun-3': (3, 1),
    'walk-gun-4': (4, 1),
    'stand' : (4, 2),
    'walk-1': (5, 2),
    'walk-2': (6, 2),
    'walk-3': (7, 2),
    'walk-4': (0, 3),
    'jump' : (1, 3)
}

class Player(pygame.sprite.Sprite):
    player_width, player_height = 35, 45

    def __init__(self, cordinate_x, cordinate_y, action):
        """
        This method will initialise a player sprite at the coordinate_x, coordinate_y,
        and the action associated with the player sprite

        # :type coordinate_x : int x coordinate of the sprite
        # :type coordinate_y : int y coordinate of the sprite
        :type action: str action assoicated with the sprite
        :type direction: str direction in which player will move
        """
        self.action = action
        """
        sprite_x = x cordinate of the image of the player in cowboy.png
        sprite_y = y cordinate of the image of the player in cowboy.png
        """
        self.sprite_x, self.sprite_y = self.x_y_in_spritesheet()

        # self.image holds the current image of the player's action, rect is the rectangular cordinate of the image
        self.image = pygame.Surface((90, 90), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        
        self.x_cord, self.y_cord = cordinate_x, cordinate_y
        self.left = False
        self.speed = 7
        self.is_jump = False
        self.velocity = 8
        self.mass = 1




    def __str__(self):
        """
        Returns the information about the player, helpful in debugging!

        :rtype: str x-coordinate - PlayerX, \n y-coordinate - PlayerY, \n action - action, \n x-coordinate - sprite-SpriteX, \n y-coordinate - sprite-SpriteY\n
        """
        return ''' x-coordinate - {}, \n y-coordinate - {},\
                \n action - {}, \n x-coordinate-sprite - {},\
                \n y-coordinate-sprite - {}\n'''.format(self.x_cord, self.y_cord, self.action, self.sprite_x, self.sprite_y)

    """
    METHODS RELATED TO MOVEMENT OF THE PLAYER
    """

    def move_right(self):
        """Moves the player right
        """
        self.left = False
        if not self.is_jump:
            if self.action not in walking_action: self.action = 'walk-1'
            self.action = next(actions)
        # End point will be useful to avoid the condition
        # where half of our character is outside the screen
        x_end_point = binder.WIDTH - (self.player_width * 2)
        self.x_cord = x_end_point if self.x_cord + self.speed > x_end_point else self.x_cord + self.speed


    def move_left(self):
        """Moves the player left
        """
        self.left = True
        if not self.is_jump:
            if self.action not in walking_action: self.action = 'walk-1'
            self.action = next(actions)
        self.x_cord = 0 if self.x_cord - self.speed < 0 else self.x_cord - self.speed

    def jump(self):
        """ This method is the event handler for jump.
        """
        self.action = 'jump'
        self.is_jump = True

    def stand(self):
        """ This method is the event handler for standing still.
        """
        if not self.is_jump: self.action = 'stand'

    def update(self):
        """ This method computes the trajectory of the jump.
        """
        if self.is_jump:
            # Calculate force (F). F = 0.5 * mass * velocity^2.
            if self.velocity > 0:
                force = ( 0.5 * self.mass * (self.velocity*self.velocity) )
            else:
                force = -( 0.5 * self.mass * (self.velocity*self.velocity) )

            # Change position
            self.y_cord = self.y_cord - force

            # Change velocity
            self.velocity = self.velocity - 1

            # If ground is reached, reset variables.
            if self.y_cord >= binder.HEIGHT - FINAL_SIZE_Y // 2:
                self.y_cord = binder.HEIGHT - FINAL_SIZE_Y // 2
                self.is_jump = False
                self.velocity = 8

    """
    METHODS RELATED TO DRAWING IMAGE OF THE PLAYER
    """

    def player_key_handler(self, pygame, event, keys):
        """This is the key handler for the player, based on the keys pressed it will execute the associated
        action for the player.
        """
        if keys[pygame.K_UP]: self.jump()
        if keys[pygame.K_LEFT]: self.move_left()
        if keys[pygame.K_RIGHT]: self.move_right()
        else : self.stand()


    def update_image(self):
        """ This method updates the image associated with the player.
        It copies the current action related image to the self.image's surface.
        """
        self.image = pygame.Surface((self.player_width, self.player_height), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.sprite_x, self.sprite_y = self.x_y_in_spritesheet()
        area_of_image = (self.sprite_x, self.sprite_y, self.player_width, self.player_height)
        self.image.blit(cowboy_sprite , (0, 0), area_of_image)
        self.image = pygame.transform.scale(self.image, (self.player_width * 2, self.player_height * 2))
        if self.left == True:
            self.image = pygame.transform.flip(self.image, 1, 0)


    def x_y_in_spritesheet(self):
        """ This method returns the x, y cordinate of the current action in cowboy.png
        """
        return WIDTH_SPRITE * ACTIONS[self.action] [0], HEIGHT_SPRITE * ACTIONS[self.action] [1]

    def get_player_image(self):
        """ Returns the image of the player
        """
        self.update_image()
        return self.image

    def player_position(self):
        """ Returns the position of the player on the main surface (screen)
        """
        return self.x_cord, self.y_cord
