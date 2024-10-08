import numpy
import pygame

from Engine.Animations.Animator import Animator
from Engine.tools import scale_image, surface_convertor, polygon_converter
import Engine.constants as cs


class MergedSpritesGroup(pygame.sprite.Group):
    def __init__(self, render_surface, image_or_animation, size: numpy.array = None, scale=None):
        super().__init__()
        self.render_surface = render_surface
        self.application = render_surface.application
        self.animator = Animator(self.application, image_or_animation, size, scale)
        self.image = self.animator.get_current_frame()
        self.render_surface.add_content(self)

    def render(self, matrix: numpy.array = None, custom_surface=None):
        sprite_image = surface_convertor(numpy.array([0, 0]), self.image, matrix, self.application)
        for sprite in self.sprites():
            point = polygon_converter(numpy.array([sprite.point]), matrix)[0]
            if custom_surface is not None:
                custom_surface.blit(sprite_image[1], point.tolist())
            else:
                self.render_surface.blit(sprite_image[1], point.tolist())

    def resize_image(self, size: numpy.array = None, scale=None):
        self.animator.resize(size, scale)
        for sprite in self.sprites():
            sprite.image = self.animator.get_current_frame()
            sprite.update_collision()

    def update(self, args):
        self.animator.update(args)
        if cs.E_EVENT in args:
            if pygame.USEREVENT + self.animator.event_number == args[cs.E_EVENT].type:
                self.image = self.animator.get_frame()
                for sprite in self.sprites():
                    sprite.image = self.image
                    sprite.update_collision()
            if cs.E_START_NEW_ANIMATION == args[cs.E_EVENT].type:
                self.image = self.animator.get_frame()
                for sprite in self.sprites():
                    sprite.image = self.image
                    sprite.update_collision()


class MergedSprite(pygame.sprite.Sprite):
    def __init__(self, point: numpy.array, group):
        super().__init__(group)
        self.image = group.image
        self.point = point
        self.application = group.application
        self.rect = self.image.get_rect()
        self.rect.x = point[0] - self.rect.width // 2
        self.rect.y = point[1] - self.rect.height // 2

    def resize(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = self.point[0] - self.rect.width // 2
        self.rect.y = self.point[1] - self.rect.height // 2

    def update_collision(self):
        self.rect = self.image.get_rect()
        self.rect.x = self.point[0] - self.rect.width // 2
        self.rect.y = self.point[1] - self.rect.height // 2
