from random import randint
import pygame, sys
from boss import Livid
import render
import generation
from entity import Player
from bestiary import Goblin
from game import GameManager
from utilities import Vec2

pygame.init()

def end_lvl(gen_, gameManager_, player_):
    gen_.generate()
    gameManager_.spawn_mob(renderer.get_rect_list(gen.the_map))
    gameManager_.create_chest()
    player_.pos = [gen_.room_list[0].center[0]*renderer.TILE_SIZE,gen_.room_list[0].center[1]*renderer.TILE_SIZE]
    player_.the_map = renderer.get_rect_list(gen.the_map)
    player_.dungeon_niv += 1

HEIGHT = 720
WIDTH = 1280

screen_size = (WIDTH, HEIGHT) #
screen = pygame.display.set_mode(screen_size)
renderer = render.Render(screen)

gen = generation.Generator([120, 120])
gen.generate()

gameManager = GameManager(gen)
gameManager.spawn_mob(renderer.get_rect_list(gen.the_map))
gameManager.create_chest()

player = Player([gen.room_list[0].center[0]*renderer.TILE_SIZE,gen.room_list[0].center[1]*renderer.TILE_SIZE ], 100, 5, 5, 50,  renderer.get_rect_list(gen.the_map))

clock = pygame.time.Clock()

while renderer.run:
    player.update([WIDTH, HEIGHT], gameManager.targets)
    gameManager.load_mob(player.pos)
    gameManager.update(player)
    gameManager.chest.update(player)

    for mob in gameManager.loaded_mob.values():
        mob.update(player)

    renderer.calculate_scroll(player)

    renderer.screen.fill((33, 38, 63))
    renderer.draw_tilemap(gen.the_map, player)
    renderer.draw_debug(clock)
    for pot in gameManager.potions:
        renderer.draw_object(pot)
    renderer.draw_player(player)

    for arrow in player.shot_arrows:
        renderer.draw_object(arrow)
        #pygame.draw.rect(screen, [255, 0, 0], pygame.Rect(arrow.rect.x - renderer.player_scroll[0], arrow.rect.y - renderer.player_scroll[1], arrow.width, arrow.height))

    for mob in gameManager.room_mob_dict.values():
        renderer.draw_object(mob)
        #pygame.draw.rect(screen, [255, 0, 0], pygame.Rect(mob.rect.x - renderer.player_scroll[0], mob.rect.y - renderer.player_scroll[1], mob.width, mob.height))

    if gameManager.isBossSpawned:
        renderer.draw_object(gameManager.livid)
        for shadow in gameManager.livid.shadows:
            renderer.draw_object(shadow)
        for projectil in gameManager.livid.daggers:
            renderer.draw_object(projectil)

    if gameManager.livid_got_killed:
        gameManager.livid_got_killed = False
        end_lvl(gen, gameManager, player)

    gameManager.check_mob_life()
    #pygame.draw.rect(screen, [0, 0, 255], player.rect)
    if len(gameManager.room_mob_dict.values()) == 0: renderer.draw_str("The candle (space)",[gen.room_list[-1].center[0]*renderer.TILE_SIZE - renderer.player_scroll[0] + 55,gen.room_list[-1].center[1]*renderer.TILE_SIZE - renderer.player_scroll[1]], (255, 255, 255), "small")
    renderer.draw_str(f"Dungeon number :{player.dungeon_niv}", [gen.room_list[0].center[0]*renderer.TILE_SIZE - renderer.player_scroll[0] - 75,gen.room_list[0].center[1]*renderer.TILE_SIZE - renderer.player_scroll[1] - 80], (255, 255, 255), "small")
    renderer.draw_hud(player, gameManager.loaded_mob, gameManager.room_mob_dict)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            renderer.run = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                gen.generate()
                player.pos = [gen.room_list[0].center[0]*renderer.TILE_SIZE,gen.room_list[0].center[1]*renderer.TILE_SIZE ]
                player.the_map = renderer.get_rect_list(gen.the_map)
                gameManager.create_chest()
                gameManager.spawn_mob(renderer.get_rect_list(gen.the_map))
            if event.key == pygame.K_SPACE:
                if Vec2.Distance(Vec2(player.pos[0], player.pos[1]), Vec2(gen.room_list[-1].center[0] *renderer.TILE_SIZE, gen.room_list[-1].center[1]*renderer.TILE_SIZE)) < 100 and len(gameManager.room_mob_dict.values()) == 0:
                    gameManager.spawn_livid(renderer.get_rect_list(gen.the_map))

        if event.type == player.PLAYER_DIE:
            gen.generate()
            gameManager.spawn_mob(renderer.get_rect_list(gen.the_map))
            gameManager.create_chest()
            player = Player([gen.room_list[0].center[0]*renderer.TILE_SIZE,gen.room_list[0].center[1]*renderer.TILE_SIZE ], 100, 5, 5, 50,  renderer.get_rect_list(gen.the_map))

    clock.tick(renderer.FPS)
