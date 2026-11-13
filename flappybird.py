import pygame
import random

pygame.init()
screen = pygame.display.set_mode((533, 375))
pygame.display.set_caption('Flappy Bird')

bg_x = 0

flappy_bird_anim = [
    pygame.transform.scale(
        pygame.image.load('icons/bird_anim/bird.png').convert_alpha(),
        (40, 50) 
    ),
    pygame.transform.scale(
        pygame.image.load('icons/bird_anim/bird2.png').convert_alpha(),
        (40, 50)  
    )
]

bird_masks = [pygame.mask.from_surface(img) for img in flappy_bird_anim]

truba_raw = pygame.image.load('icons/truba.png').convert_alpha()
all_truba_in_game = []
truba_timer = pygame.USEREVENT + 1  
pygame.time.set_timer(truba_timer, 1200)

label=pygame.font.Font('fonts/Opensans.ttf')
lose_label=label.render('Нажмите ПРОБЕЛ или К что бы продолжить', False, (115, 132, 148))

all_truba2_in_game = []

flappy_bird_anim_count = 0.0 
truba_x = 610
truba_y = 150  
truba2_x = 600
truba2_y = -100 
bird_x = 246
bird_y = 162
gravity = 3
jump_strengh = -25

bg = pygame.image.load('icons/fb_bg.jpg').convert()

running = True
gameplay = True
clock = pygame.time.Clock()

while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
           if (event.key == pygame.K_SPACE or event.key == pygame.K_w) and gameplay and bird_y > 0:
               bird_y += jump_strengh
           if (event.key==pygame.K_SPACE or event.key==pygame.K_r) and not gameplay:
              gameplay=True
              all_truba_in_game.clear()
              all_truba2_in_game.clear()
              bird_x=246
              bird_y=162
        if event.type == pygame.MOUSEBUTTONDOWN:
           if event.button == 1 and gameplay:
               bird_y += jump_strengh

        if event.type == truba_timer and gameplay:

            GAP = 110 

            bottom_height = random.randint(60, 200)
            truba_scaled = pygame.transform.scale(truba_raw, (90, bottom_height))
            bottom_y = 375 - bottom_height 
            orig_rect2 = truba_scaled.get_rect(topleft=(truba_x, bottom_y))
            t_mask = pygame.mask.from_surface(truba_scaled)
            all_truba_in_game.append((orig_rect2, t_mask, truba_scaled))

            top_height = 375 - bottom_height - GAP
            truba_flipped = pygame.transform.flip(truba_raw, False, True)
            truba2_scaled = pygame.transform.scale(truba_flipped, (90, top_height))
            # Верхняя труба ВСЕГДА начинается от верхнего края (0)
            orig_rect3 = truba2_scaled.get_rect(topleft=(truba_x, 0)) 
            t_mask2 = pygame.mask.from_surface(truba2_scaled)
            all_truba2_in_game.append((orig_rect3, t_mask2, truba2_scaled))


    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 533, 0))
    
    if gameplay:
        bg_x -= 1
        if bg_x <= -533:
            bg_x = 0
        bird_y += gravity
        current_frame = int(flappy_bird_anim_count)  
        screen.blit(flappy_bird_anim[current_frame], (bird_x, bird_y))
        if bird_y >= 305:
            gameplay = False
            print('Game over: Упал на землю')

        if all_truba_in_game:
           for i, (el, pipe_mask, pipe_surf) in enumerate(all_truba_in_game[::-1]):
              screen.blit(pipe_surf, el)
              el.x -= 3
              if el.x < -110:
                 all_truba_in_game.pop(len(all_truba_in_game) - 1 - i)

              offset_x = el.x - bird_x
              offset_y = el.y - bird_y

              current_mask = bird_masks[int(flappy_bird_anim_count)]

              if current_mask.overlap(pipe_mask, (offset_x, offset_y)):
                  gameplay = False 
                  print('Game over: Столкновение с нижней трубой')

        if all_truba2_in_game:
           for i, (el, pipe_mask, pipe_surf) in enumerate(all_truba2_in_game[::-1]):
              screen.blit(pipe_surf, el)
              el.x -= 3
              if el.x < -110:
                 all_truba2_in_game.pop(len(all_truba2_in_game) - 1 - i)

              offset_x = el.x - bird_x
              offset_y = el.y - bird_y

              current_mask = bird_masks[int(flappy_bird_anim_count)]

              if current_mask.overlap(pipe_mask, (offset_x, offset_y)):
                  gameplay = False 
                  print('Game over: Столкновение с верхней трубой')

        flappy_bird_anim_count += 0.15
        if flappy_bird_anim_count >= len(flappy_bird_anim):
            flappy_bird_anim_count = 0.0


    else:
       screen.fill((87,88,89))
       screen.blit(lose_label,(100,0))

    pygame.display.update()
    clock.tick(25)

pygame.quit() 


