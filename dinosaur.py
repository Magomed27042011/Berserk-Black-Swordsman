import pygame
import random
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption('Google dino')
dino_x = 50
dino_y = 258
bg_y = 0
bg_x = 0
ground_x = 0
ground_y = 300
pteradon_y=400
pteradon_x=445
cactus_speed=5
pteradon_speed=5
sjet=0
record_sjet=0
dino_font=pygame.font.Font('fonts/DinosaurFont.ttf')
dino_big_font=pygame.font.Font('fonts/DinosaurFont.ttf',40)
lose_label=dino_big_font.render('Game over', False, (115, 132, 148))
restart_label=dino_font.render('Press Space or R to play', False, (115, 132, 148))

overlay=pygame.Surface((600,400))
overlay.set_alpha(1)
overlay.fill((193, 196, 192))

bg = pygame.image.load('icons/white_bg.jpg')
all_cactus_in_game=[]
spawn_timer=pygame.USEREVENT+1
pygame.time.set_timer(spawn_timer,random.randint(1500,2500))
all_pteradon_in_game=[]
sjet_timer=pygame.USEREVENT+2
pygame.time.set_timer(sjet_timer,100)

cactus_anim1=pygame.transform.scale(pygame.image.load('icons/Cactus/Cactus-1.png').convert_alpha(),(32,62))
cactus_anim2=pygame.transform.scale(pygame.image.load('icons/Cactus/Cactus-2.png').convert_alpha(),(20,42))
cactus_anim3=pygame.transform.scale(pygame.image.load('icons/Cactus/Cactus-3.png').convert_alpha(),(62,59))
cactus_anim4=pygame.transform.scale(pygame.image.load('icons/Cactus/Cactus-4.png').convert_alpha(),(59,59))
cactus_anim5=pygame.transform.scale(pygame.image.load('icons/Cactus/Cactus-5.png').convert_alpha(),(41,42))
cactus_images = [cactus_anim1, cactus_anim2, cactus_anim3, cactus_anim4, cactus_anim5]
pterodactel_img=[
    pygame.transform.scale(pygame.image.load('icons/pterodaktel/Pterodactel3.png').convert_alpha(),(70, 70)),
    pygame.transform.scale(pygame.image.load('icons/pterodaktel/Pterodactel4.png').convert_alpha(), (70, 70))
]
dinosaur_anim=[
    pygame.transform.scale(pygame.image.load('icons/dinosaur/Dino1.png').convert_alpha(),(44, 48)),
    pygame.transform.scale(pygame.image.load('icons/dinosaur/Dino2.png').convert_alpha(), (44, 48)),
    pygame.transform.scale(pygame.image.load('icons/dinosaur/Dino3.png').convert_alpha(), (44, 48))
]
meteorid_anim_count=0.0
dinosaur_anim_count=0.0
ground_img=pygame.image.load('icons/Ground.png')
ground=pygame.transform.scale(ground_img,(600,12))

is_jump = False
jump_count = 9.5

player_rect=pygame.Rect(dino_x, dino_y, 44, 48)

runing = True
gameplay = True
clock = pygame.time.Clock()
while runing:
    sjet_label2=dino_font.render(f'Your score:{sjet}', False, (115, 132, 148))
    sjet_label=dino_font.render(f'score:{sjet}', False, (115, 132, 148))
    record_label=dino_font.render(f'best:{record_sjet}', False, (115, 132, 148))
    choise=random.choice([True,False])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
        if event.type==sjet_timer and gameplay==True:
            sjet+=1
        if event.type==spawn_timer and gameplay:
          if choise==True:
            cactus_image = random.choice(cactus_images)
            cactus_rect = pygame.Rect(
                610, 
                ground_y + 12 - cactus_image.get_height(),
                cactus_image.get_width(), 
                cactus_image.get_height()
            )
            all_cactus_in_game.append([cactus_rect, cactus_image])
          else:
                all_pteradon_in_game.append({
                    "rect": pygame.Rect(610,245,70,70),
                    'anim_count': 0.0
                })
          pygame.time.set_timer(spawn_timer,random.randint(1200,1900))
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            if gameplay==True:
              is_jump=True

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_SPACE] or keys[pygame.K_r]) and gameplay==False:
        sjet=0
        cactus_speed=5
        pteradon_speed=5
        gameplay=True
    if not is_jump:
        if keys[pygame.K_SPACE]:
            is_jump = True
            jump_count = 9.5 
    else:
        if jump_count >= -9.5:
            if jump_count > 0:
                dino_y -= (jump_count ** 2) / 2
            else:
                dino_y += (jump_count ** 2) / 2
            jump_count -= 0.8
        else:
            is_jump = False
            dino_y = 258
            jump_count = 9.5
    player_rect.y=dino_y
    if gameplay==True:
        current_sprite = dinosaur_anim[int(dinosaur_anim_count)]
        dinosaur_anim_count += 0.20
        if dinosaur_anim_count >= len(dinosaur_anim):
            dinosaur_anim_count = 0.0
        screen.blit(bg, (bg_x, bg_y))
        screen.blit(bg, (bg_x + 600, bg_y))
        screen.blit(current_sprite, (dino_x, dino_y))
        screen.blit(sjet_label,(10,10))
        screen.blit(record_label,(10,40))
        bg_x -= 5
        if bg_x <= -600:
            bg_x = 0

        if all_cactus_in_game:
            for cactus_data in all_cactus_in_game[:]:
              cactus_rect = cactus_data[0]
              cactus_image = cactus_data[1]
              
              screen.blit(cactus_image, cactus_rect)
              cactus_rect.x -= cactus_speed
              
              if cactus_rect.x <= -30:
               all_cactus_in_game.remove(cactus_data)
              if sjet>record_sjet:
                     record_sjet=sjet
              if player_rect.colliderect(cactus_rect):
                  cactus_speed=0
                  gameplay=False

        if all_pteradon_in_game:
         for el in all_pteradon_in_game[:]:
            current_frame = pterodactel_img[int(el["anim_count"])]
            screen.blit(current_frame, el["rect"])
            el["rect"].x -= pteradon_speed
            el["anim_count"] += 0.15
            if el["anim_count"] >= len(pterodactel_img):
                el["anim_count"] = 0.0
            if el['rect'].x<=-30:
               all_pteradon_in_game.remove(el)
            if sjet>record_sjet:
                     record_sjet=sjet
            pteradon_hitbox=el['rect'].inflate(-30,-30)
            if player_rect.colliderect(pteradon_hitbox):
                  pteradon_speed=0
                  gameplay=False
        
        screen.blit(ground,(ground_x,ground_y))
        screen.blit(ground,(ground_x+600,ground_y))
        ground_x-=5
        if ground_x<=-600:
            ground_x=0
    else:
        screen.blit(overlay,(0,0))
        lose_rect = lose_label.get_rect(center=(300, 150))
        screen.blit(lose_label,lose_rect)
        restart_rect = restart_label.get_rect(center=(300, 220))
        screen.blit(restart_label,restart_rect)
        sjet_rect = sjet_label.get_rect(center=(300, 290))
        screen.blit(sjet_label2,sjet_rect)
        all_cactus_in_game.clear()
        all_pteradon_in_game.clear()

    clock.tick(40)
    pygame.display.update()

pygame.quit()