from random import randint
import pygame, sys
import render
import generation
from entity import Player
from bestiary import Goblin
from game import GameManager

pygame.init()

HEIGHT = 720
WIDTH = 1280

screen_size = (WIDTH, HEIGHT) #
screen = pygame.display.set_mode(screen_size)
renderer = render.Render(screen)


gen = generation.Generator([120, 120])
gen.generate()

gameManager = GameManager(gen)
gameManager.spawn_mob(renderer.get_rect_list(gen.the_map))

player = Player([gen.room_list[0].center[0]*renderer.TILE_SIZE,gen.room_list[0].center[1]*renderer.TILE_SIZE ], 100, 5, 5, 10,  renderer.get_rect_list(gen.the_map))
goblin_test = Goblin([gen.room_list[1].center[0]*renderer.TILE_SIZE + randint(0, 100),gen.room_list[1].center[1]*renderer.TILE_SIZE ], 20, 0, 2, 2, renderer.get_rect_list(gen.the_map))

clock = pygame.time.Clock()

while renderer.run:
    player.update([WIDTH, HEIGHT])
    #gameManager.load_mob(player.pos)
    for mob in gameManager.loaded_mob:
        mob.update(player)
    renderer.calculate_scroll(player)


    renderer.screen.fill((33, 38, 63))
    renderer.draw_tilemap(gen.the_map, player)
    renderer.draw_debug(clock)
    renderer.draw_player(player)
    for mob in gameManager.loaded_mob:
        renderer.draw_object(mob)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            renderer.run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gen.generate()
                player.pos = [gen.room_list[0].center[0]*renderer.TILE_SIZE,gen.room_list[0].center[1]*renderer.TILE_SIZE ]
                player.the_map = renderer.get_rect_list(gen.the_map)

    clock.tick(renderer.FPS)
