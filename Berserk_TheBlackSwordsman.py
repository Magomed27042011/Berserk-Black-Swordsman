import pygame #first commit 
#first

clock = pygame.time.Clock()

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1100, 705))
pygame.display.set_caption("Berserk — The Black Swordsman")
bg_anim = [
    pygame.image.load('Berserk icons/bg_img.png').convert_alpha(),
    pygame.transform.scale(pygame.image.load('Berserk icons/bg_img2.png').convert_alpha(),(1100,705)),
    pygame.transform.scale(pygame.image.load('Berserk icons/bg_img3.png').convert_alpha(),(1100,705)),
    pygame.transform.scale(pygame.image.load('Berserk icons/bg_img4.png').convert_alpha(),(1100,705)),
    pygame.transform.scale(pygame.image.load('Berserk icons/bg_img5.png').convert_alpha(),(1100,705))
]
bg_animation_delay = 900
bg_anim_count = 0
start_bg = pygame.image.load('Berserk icons/start_bg.png').convert_alpha()
pygame.display.set_icon(pygame.image.load("Berserk icons/icon.jpg"))
gats_anim = [
    pygame.transform.scale(pygame.image.load('Berserk icons/berserk_img1.png').convert_alpha(),(179, 164)),
    pygame.transform.scale(pygame.image.load('Berserk icons/berserk_img2.png').convert_alpha(),(179, 164)),
    pygame.transform.scale(pygame.image.load('Berserk icons/berserk_img3.png').convert_alpha(),(179, 164)),
    pygame.transform.scale(pygame.image.load('Berserk icons/berserk_img4.png').convert_alpha(),(179, 164)),
    pygame.transform.scale(pygame.image.load('Berserk icons/berserk_img5.png').convert_alpha(),(179, 164))
]
guts_anim_right = [
    pygame.transform.scale(pygame.image.load('Berserk icons/berserk_img6.png').convert_alpha(),(179, 164)),
    #pygame.transform.scale(pygame.image.load('icons/Berserk icons/berserk_img7.png').convert_alpha(),(179, 164)),
    pygame.transform.scale(pygame.image.load('Berserk icons/berserk_img8.png').convert_alpha(),(179, 164))
]
apostol_anim = [
    pygame.transform.scale(pygame.image.load('Berserk icons/appostol1.png').convert_alpha(),(179, 164)),
    pygame.transform.scale(pygame.image.load('Berserk icons/appostol2.png').convert_alpha(),(179, 164)),
    pygame.transform.scale(pygame.image.load('Berserk icons/appostol3.png').convert_alpha(),(179, 164))
]
appostol_anim_count = 0
appostol_x = 1000
appostol_y = 450
appostol_timer = pygame.USEREVENT + 1
appostol_speed = 2
pygame.time.set_timer(appostol_timer, 2200)
all_appostols_in_game = []
player_anim_count = 1
player_anim_count2 = 0
player_speed = 1
guts_x = 230
guts_y = 435
animation_dielay = 180
bg_last_update = pygame.time.get_ticks()
last_update = pygame.time.get_ticks()
last_update2 = pygame.time.get_ticks()
appostol_last_update = pygame.time.get_ticks()
overlay = pygame.Surface((1100,705))
overlay.set_alpha(65)
overlay.fill((18, 12, 30))

label = pygame.font.Font('fonts/Cinzel-Bold.ttf', 48)
start_label = label.render("PLAY" ,False, (150, 35, 45))
start_label_rect = start_label.get_rect(center=(550,330))
close_label = label.render("CLOSE" ,False, (150, 35, 45))
close_label_rect = start_label.get_rect(center=(527,390))

Guts = 'sounds/Berserk1.mp3'
pygame.mixer.music.load(Guts)
pygame.mixer.music.play(-1)
Murder = 'sounds/Berserk3.mp3'

gameplay = "start_mode"
runing = True

while runing:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False 
        if event.type == appostol_timer and gameplay == 'game':
           all_appostols_in_game.append([appostol_x, appostol_y])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            if start_label_rect.collidepoint(event.pos):
                gameplay = "game"
                pygame.mixer.music.stop()
                pygame.mixer.music.load(Murder)
                pygame.mixer.music.set_volume(0.35)
                pygame.mixer.music.play(-1)
            elif close_label_rect.collidepoint(event.pos):
                runing=False

    if gameplay == "start_mode":
        screen.blit(start_bg,(0,0))
        screen.blit(overlay,(0,0))
        screen.blit(start_label,start_label_rect)
        screen.blit(close_label,close_label_rect)
    elif gameplay == "game":

     current_time = pygame.time.get_ticks()
     if current_time - bg_last_update >= bg_animation_delay:
        bg_anim_count += 1

        if bg_anim_count >= len(bg_anim):
            bg_anim_count = 0

        bg_last_update = current_time

     current_sprite = bg_anim[bg_anim_count]
     screen.blit(current_sprite, (0, 0))
     if current_time - last_update >= animation_dielay:
        player_anim_count += 1

        if player_anim_count >= len(gats_anim):
            player_anim_count = 0

        last_update = current_time
     if current_time - appostol_last_update >= animation_dielay:
        appostol_anim_count += 1

        if appostol_anim_count >= len(apostol_anim):
           appostol_anim_count = 0
        appostol_last_update = current_time
     if keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_LEFT] or keys[pygame.K_a]:
      current_sprite = guts_anim_right[player_anim_count2]
     else:
        current_sprite = gats_anim[player_anim_count]
     screen.blit(current_sprite,(guts_x,guts_y))
     for appostol in all_appostols_in_game:
        appostol[0] -= appostol_speed
        screen.blit(
           apostol_anim[appostol_anim_count],
           (appostol[0],appostol[1])
            )
        all_appostols_in_game = [
           appostol for appostol in all_appostols_in_game
           if appostol[0] > -179
        ]
     
     if (keys[pygame.K_RIGHT ] or keys[pygame.K_d]) and guts_x < 750:
        guts_x+=player_speed
        if current_time - last_update2 >= animation_dielay:
            player_anim_count2 +=1
            if player_anim_count2>=len(guts_anim_right):
             player_anim_count2 = 0
            last_update2 = current_time
     if (keys[pygame.K_LEFT ] or keys[pygame.K_a]) and guts_x > 0:
        guts_x-=player_speed
        if current_time - last_update2 >= animation_dielay:
            player_anim_count2 +=1
            if player_anim_count2>=len(guts_anim_right):
             player_anim_count2 = 0
            last_update2 = current_time
    pygame.display.update()
    clock.tick(90)
pygame.quit()