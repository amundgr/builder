import json
import os
import math

import pygame as pg
from pygame.locals import *

SPRITE_PATH = "graphics/sprites"
empty = pg.Color(0,0,0,0)

class Sprite(pg.sprite.Sprite):
    def __init__(self, position, sprite_name, sprite_folder, scale=1, tag=""):
        self.tag = tag
        self.sprite_name = sprite_name
        pg.sprite.Sprite.__init__(self)
        self.file_path = os.path.join(sprite_folder, sprite_name)
        self.sheet = pg.image.load(f"{self.file_path}.png").convert_alpha()
        self.x, self.y = position
        with open(f"{self.file_path}.json") as fp:
            self.sheet_info = json.load(fp)
        
        #Assumes frames in a line
        self.length = len(self.sheet_info["frames"])

        #Assumes that all frames are the same size
        self.w = self.sheet_info["frames"][0]["frame"]["w"]
        self.h = self.sheet_info["frames"][0]["frame"]["h"]
    
        
        #Scale sprite
        self.scale = scale
        self.w = int(self.w * scale)
        self.h = int(self.h * scale)
        new_w_sheet = int(self.sheet_info["meta"]["size"]["w"] * scale)
        new_h_sheet = int(self.sheet_info["meta"]["size"]["h"] * scale)
        self.sheet = pg.transform.scale(self.sheet, (new_w_sheet, new_h_sheet))


        self.idx = 0
        self._generate_rects()   
        self.image = pg.Surface((self.w, self.h)).convert_alpha()
        #self.image.set_alpha(0)
        self.rect = pg.Rect(self.x, self.y, self.w, self.h)
    
    def move_to(self, position=(0,0)):
        self.rect.x = position[0]
        self.rect.y = position[1]

    def move(self, movement=(0,0)):
        self.rect.x += movement[0]
        self.rect.y += movement[1]

    def _generate_rects(self):
        self.rects = []
        for frame in self.sheet_info["frames"]:
            val = frame["frame"]
            self.rects.append(pg.Rect((int(val["x"] * self.scale), 
                                    int(val["y"] * self.scale), 
                                    int(val["w"] * self.scale), 
                                    int(val["h"] * self.scale))))
        
        
    def update(self):
        self.image.fill(empty)
        self.image.blit(self.sheet, (self.x,self.y), self.rects[self.idx])
        self.idx += 1 if self.idx < self.length-1 else -self.idx

class Lamp(Sprite):
    def __init__(self, position=(0,0), scale=1, tag=""):
        Sprite.__init__(self, sprite_name="Lamp", sprite_folder=SPRITE_PATH, position=position, scale=scale, tag=tag)
        self.light = Light(position=position, scale=scale)
        self._move_light()
        self.r = int(self.w/2)
    
    def _move_light(self, offset=(-0.0,-0)):
        self.light.rect.center = (self.rect.center[0] + int(offset[0] * self.scale), 
                                  self.rect.center[1] + int(offset[1] * self.scale))

    def move_to(self, position=(0,0)):
        super().move(position=position)
        self._move_light()

    def calc_dist(self, other):
        return math.sqrt((other.rect.center[0] - self.rect.center[0]) ** 2 + (other.rect.center[1] - self.rect.center[1]) ** 2)

    def move(self, movement=(0,0)):
        self.rect.x += movement[0]
        self.rect.y += movement[1]
        for group in self.groups():
            for sprite in group:
                if not sprite is self:
                    if sprite.rect.colliderect(self.rect):
                        if self.calc_dist(sprite) < (self.r + sprite.r):
                            self.rect.x -= movement[0]
                            if self.calc_dist(sprite) < (self.r + sprite.r):
                                self.rect.x += movement[0]
                                self.rect.y -= movement[1]
                                if self.calc_dist(sprite) < (self.r + sprite.r):
                                    self.rect.x -= movement[0]
                            

        self._move_light()

class Light(Sprite):
    def __init__(self, position=(0,0), scale=1):
        Sprite.__init__(self, sprite_name="Light", sprite_folder=SPRITE_PATH, position=position, scale=scale*2)
        self.light_image = self.image.copy()

    def update(self):
        self.image.fill((0,0,0,255))
        self.image.blit(self.sheet, (self.x,self.y), self.rects[self.idx], special_flags=BLEND_RGBA_SUB)
        self.idx += 1 if self.idx < self.length-1 else -self.idx