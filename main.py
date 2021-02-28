import sys
import math

import pygame as pg

from game_objects import Lamp
from pygame.locals import *

size = (1000, 1000)
pg.init()
main_screen = pg.display.set_mode(size)
light_surface = pg.Surface(size, pg.SRCALPHA)
game_object_surface = pg.Surface(size, pg.SRCALPHA)
clock = pg.time.Clock()

SCREEN_UPDATE = pg.USEREVENT
pg.time.set_timer(SCREEN_UPDATE, 150)

game_object_group = pg.sprite.Group()
light_group = pg.sprite.Group()
lamp = Lamp(position=(0,0), scale=4, tag="lamp_1")
lamp.rect.center  = (250,250)
lamp.move((0,0))

game_object_group.add(lamp)
light_group.add(lamp.light)

lamp2 = Lamp(position=(0,0), scale=4, tag="lamp_2")
lamp2.rect.center  = (500,500)
lamp2.move((0,0))

game_object_group.add(lamp2)
#light_group.add(lamp2.light)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                lamp.move((0,-10))
            if event.key == pg.K_s:
                lamp.move((0,10))
            if event.key == pg.K_d:
                lamp.move((10,0))
            if event.key == pg.K_a:
                lamp.move((-10,0))

    # Hard coed moving
    
    move_speed = 10
    mouse_pos = pg.mouse.get_pos()
    dist = (mouse_pos[0] - lamp.rect.centerx, mouse_pos[1] - lamp.rect.centery)
    if (abs(dist[0]) <= move_speed):
        dist = (0, dist[1])
    if (abs(dist[1]) <= move_speed):
        dist = (dist[0], 0)
    
    abs_dist = math.sqrt(dist[0]**2 + dist[1]**2)
    if abs_dist:
        normalized_mouse_pos = (int(move_speed * dist[0]/abs_dist), int(move_speed * dist[1]/abs_dist))
        lamp.move(normalized_mouse_pos)
    

    main_screen.fill((100, 100, 100, 255))
    game_object_surface.fill((100,100,100,255))
    light_surface.fill((0,0,0,255))
    #lamp.move_to((0, 0))
    game_object_group.update()
    for i, obj in enumerate(sorted(game_object_group, key=lambda s: s.rect.y, reverse=False)):
        game_object_surface.blit(obj.image, (obj.rect.x, obj.rect.y))
    #game_object_group.draw(game_object_surface)
    light_group.update()
    #light_group.draw(light_surface)
    #print("Edge:", lamp.light.image.get_at((0, 0)))
    #print("Center:", lamp.light.image.get_at((210, 0)))
    main_screen.blit(game_object_surface, (0,0))
    for light in light_group:
        light_surface.blit(light.image, (light.rect.x, light.rect.y), special_flags=BLEND_RGBA_MIN)
    main_screen.blit(light_surface, (0,0))
    pg.display.update()
    clock.tick(20)