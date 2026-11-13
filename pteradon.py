import pygame
import random

pygame.init()

screen = pygame.display.set_mode((926, 560))
pygame.display.set_caption('Pteradon')

bg_img = pygame.image.load('icons/background.jpg').convert()
bg = pygame.transform.scale(bg_img, (926, 560))

diamond_img = pygame.image.load('icons/diamond.png').convert_alpha()
diamond = pygame.transform.scale(diamond_img, (30, 30))
diamond_timer = pygame.USEREVENT + 3
pygame.time.set_timer(diamond_timer, 3000)

meteorid_img = pygame.image.load('icons/meteorid2.png').convert_alpha()
meteorid = pygame.transform.scale(meteorid_img, (70, 70))

heart_img = pygame.image.load('icons/heart1.png').convert_alpha()
heart = pygame.transform.scale(heart_img, (45, 45))

pteradon_anim = [
    pygame.transform.scale(pygame.image.load('icons/pteradon_fly/pteradon1.png').convert_alpha(), (120, 130)),
    pygame.transform.scale(pygame.image.load('icons/pteradon_fly/pteradon2.png').convert_alpha(), (120, 130)),
    pygame.transform.scale(pygame.image.load('icons/pteradon_fly/pteradon3.png').convert_alpha(), (120, 130))
]
meteorid_anim = [
    pygame.transform.scale(pygame.image.load('icons/meteorid_anim/meteorid1.png').convert_alpha(), (70, 70)),
    pygame.transform.scale(pygame.image.load('icons/meteorid_anim/meteorid2.png').convert_alpha(), (70, 70)),
    pygame.transform.scale(pygame.image.load('icons/meteorid_anim/meteorid3.png').convert_alpha(), (70, 70))
]
meteorid_anim_count = 0.0
pteradon_anim_count = 0.0

meteorid_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteorid_timer, 1000)

heard_timer = pygame.USEREVENT + 2
pygame.time.set_timer(heard_timer, 7000)

all_heard_in_game = []
all_meteorid_in_game = []
all_diamond_in_game = []

label = pygame.font.Font('fonts/Opensans.ttf', 40)
label_small = pygame.font.Font('fonts/Opensans.ttf', 30)

overlay = pygame.Surface((926, 560))
overlay.set_alpha(150)
overlay.fill((0, 0, 30))

close_label = label.render('Закрыть', False, (193, 196, 199))
close_label_rect = close_label.get_rect(center=(463, 350))

restart_label = label.render('Играть', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(center=(463, 250)) 

Level_label = label_small.render('Выбери уровень сложности', False, (193, 196, 199))
Level_label_rect = Level_label.get_rect(center=(463, 150))

restart_label3 = label.render('Легкий', False, (115, 132, 148))
restart_label4 = label.render('Средний', False, (115, 132, 148))
restart_label5 = label.render('Сложный', False, (115, 132, 148))

restart_label_rect3 = restart_label3.get_rect(center=(463, 280))
restart_label_rect4 = restart_label4.get_rect(center=(463, 350))
restart_label_rect5 = restart_label5.get_rect(center=(463, 420))

lose_label = label.render('Вы проиграли!', False, (193, 196, 199))
lose_label_rect = lose_label.get_rect(center=(463, 200))

restart_label2 = label.render('Играть заново', False, (115, 132, 148))
restart_label2_rect = restart_label2.get_rect(center=(463, 320))

player_speed = 5
heard_speed = 3
meteorid_speed = 5
diamond_speed = 3
bg_speed = 1

pygame.mixer.music.load('sounds/sound3.mp3')
pygame.mixer.music.play(-1)

bg_x = 0
menu_bg_x = 0
pteradon_hard = 3
player_x = 50
player_y = 220
score = 0

clock = pygame.time.Clock()
running = True
gameplay = 'start mode'

while running:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    
    if gameplay == 'game':
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + 926, 0))
        bg_x -= bg_speed
        if bg_x <= -926:
            bg_x = 0
    else:
        screen.blit(bg, (menu_bg_x, 0))
        screen.blit(bg, (menu_bg_x + 926, 0))
        menu_bg_x -= 0.5
        if menu_bg_x <= -926:
            menu_bg_x = 0
        screen.blit(overlay, (0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if gameplay == 'game':
            if event.type == heard_timer:
                random_y = random.randint(10, 450 - 45)
                star_rect = heart.get_rect(topleft=(926, random_y))
                all_heard_in_game.append(star_rect)

            if event.type == diamond_timer:
                random_y = random.randint(10, 450 - 45)
                star_rect = diamond.get_rect(topleft=(926, random_y))
                all_diamond_in_game.append(star_rect)

            if event.type == meteorid_timer:
                random_y = random.randint(10, 450 - 70)
                all_meteorid_in_game.append({
                    "rect": meteorid_anim[0].get_rect(topleft=(926, random_y)),
                    'anim_count': 0.0
                })
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gameplay == 'start mode':
                if restart_label_rect.collidepoint(event.pos):
                    gameplay = 'dificul mode'
                if close_label_rect.collidepoint(event.pos):
                    running = False
                    
            elif gameplay == 'dificul mode':
                if restart_label_rect3.collidepoint(event.pos):
                    player_speed = 5
                    heard_speed = 2
                    meteorid_speed = 3
                    diamond_speed = 2
                    bg_speed = 1
                    pteradon_hard = 5
                    gameplay = 'game'
                if restart_label_rect4.collidepoint(event.pos):
                    player_speed = 3
                    heard_speed = 4
                    meteorid_speed = 6
                    diamond_speed = 4
                    bg_speed = 2
                    pteradon_hard = 3
                    gameplay = 'game'
                if restart_label_rect5.collidepoint(event.pos):
                    player_speed = 2
                    heard_speed = 6
                    meteorid_speed = 10
                    diamond_speed = 6
                    bg_speed = 3
                    pteradon_hard = 2
                    gameplay = 'game'
                    
            elif gameplay == 'game_over':
                if restart_label2_rect.collidepoint(event.pos):
                    gameplay = 'game'
                    player_x = 50
                    player_y = 220
                    pteradon_hard = 3
                    score = 0
                    all_meteorid_in_game.clear()
                    all_heard_in_game.clear()
                    all_diamond_in_game.clear()
                    pygame.mixer.music.play(-1)

    if gameplay == 'start mode':
        screen.blit(restart_label, restart_label_rect)  
        screen.blit(close_label, close_label_rect) 
        all_meteorid_in_game.clear()
        
    elif gameplay == 'dificul mode':
        screen.blit(Level_label, Level_label_rect)
        screen.blit(restart_label3, restart_label_rect3)
        screen.blit(restart_label4, restart_label_rect4)
        screen.blit(restart_label5, restart_label_rect5)
        all_meteorid_in_game.clear()

    elif gameplay == 'game':
        diamond_label = label.render(f'{score}', False, (255, 255, 255))

        current_sprite = pteradon_anim[int(pteradon_anim_count)]
        orig_rect = current_sprite.get_rect(topleft=(player_x, player_y))
        pteradon_rect = orig_rect.inflate(-50, -50)
        pteradon_rect.center = orig_rect.center
        screen.blit(current_sprite, (player_x, player_y))
        pteradon_anim_count += 0.15
        if pteradon_anim_count >= len(pteradon_anim):
            pteradon_anim_count = 0.0

        if keys[pygame.K_w] and player_y > 10:
            player_y -= player_speed
        if keys[pygame.K_s] and player_y < 330:
            player_y += player_speed
        if keys[pygame.K_a] and player_x > 10:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < 800:
            player_x += player_speed

        for i in range(pteradon_hard):
            screen.blit(heart, (20 + i * 50, 20))

        screen.blit(diamond, (25, 80))
        screen.blit(diamond_label, (70, 70))

        for el in all_meteorid_in_game[:]:
            current_meteor_frame = meteorid_anim[int(el["anim_count"])]
            screen.blit(current_meteor_frame, el["rect"])
            el["rect"].x -= meteorid_speed
            el["anim_count"] += 0.15
            if el["anim_count"] >= len(meteorid_anim):
                el["anim_count"] = 0.0
            if el['rect'].right < 0:
                all_meteorid_in_game.remove(el)
            if pteradon_rect.colliderect(el['rect']):
                pteradon_hard -= 1
                all_meteorid_in_game.remove(el)
                if pteradon_hard <= 0:
                    gameplay = "game_over"
                    pygame.mixer.music.stop()

        for el_heart in all_heard_in_game[:]:
            screen.blit(heart, el_heart)
            el_heart.x -= heard_speed
            if el_heart.right < 0:
                all_heard_in_game.remove(el_heart)
            if pteradon_rect.colliderect(el_heart):
                if pteradon_hard < 5:
                    pteradon_hard += 1
                all_heard_in_game.remove(el_heart)
                
        for el_diamond in all_diamond_in_game[:]:
            screen.blit(diamond, el_diamond)
            el_diamond.x -= diamond_speed
            if el_diamond.right < 0:
                all_diamond_in_game.remove(el_diamond)
            if pteradon_rect.colliderect(el_diamond):
                score += 1
                all_diamond_in_game.remove(el_diamond)

    else: 
        screen.blit(lose_label, lose_label_rect)
        screen.blit(restart_label2, restart_label2_rect)
        all_meteorid_in_game.clear()
        all_diamond_in_game.clear()
        all_heard_in_game.clear()

    pygame.display.update()

pygame.quit()

