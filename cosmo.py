import pygame
import random

pygame.init()

screen = pygame.display.set_mode((450, 750))
pygame.display.set_caption('Cosmo Shuttl')

bg = pygame.image.load('icons/cosmo_bg.png').convert()
player_img = pygame.image.load('icons/shuttl.png').convert_alpha()
player = pygame.transform.scale(player_img, (180, 180))

overlay=pygame.Surface((450,750))
overlay.set_alpha(150)
overlay.fill((0,0,30))

diamond_img = pygame.image.load('icons/diamond.png').convert_alpha()
diamond = pygame.transform.scale(diamond_img, (30, 30))
diamond_timer = pygame.USEREVENT + 4
pygame.time.set_timer(diamond_timer, 3000)
all_diamond_in_game=[]

meteorid_img = pygame.image.load('icons/meteorid.png').convert_alpha()
all_meteorid_in_game = []

pteradon_hard = 3
heart_img = pygame.image.load('icons/heart1.png').convert_alpha()
heart = pygame.transform.scale(heart_img, (45, 45))
heard_timer = pygame.USEREVENT + 3
pygame.time.set_timer(heard_timer, 7000)
all_heard_in_game = []

star_img = pygame.image.load('icons/Star.png').convert_alpha()
star_timer = pygame.USEREVENT + 2
star_size = pygame.transform.scale(star_img, (30, 30))
pygame.time.set_timer(star_timer, 10000)
all_stars_in_game = []

bullet_img = pygame.image.load('icons/bullet.png').convert_alpha()
bullet = pygame.transform.scale(bullet_img, (20, 40))
bullets = []

label = pygame.font.Font('fonts/Opensans.ttf', 40)
label_small=pygame.font.Font('fonts/Opensans.ttf',30)

restart_label2 = label.render('Играть', False, (115, 132, 148))
restart_label_rect2 = restart_label2.get_rect(center=(225, 250))

close_label = label.render('Закрыть', False, (193, 196, 199))
close_label_rect = close_label.get_rect(center=(225,350))

Level_label = label_small.render('Выбери уровень сложности', False, (193, 196, 199))
Level_label_rect = Level_label.get_rect(center=(225,200))
restart_label3 = label.render('Легкий', False, (115, 132, 148))
restart_label4 = label.render('Средний', False, (115, 132, 148))
restart_label5 = label.render('Сложный', False, (115, 132, 148))

restart_label_rect3 = restart_label3.get_rect(center=(225, 350))
restart_label_rect4 = restart_label4.get_rect(center=(225, 420))
restart_label_rect5 = restart_label5.get_rect(center=(225, 490))

lose_label = label.render('Вы проиграли!', False, (193, 196, 199))
restart_label = label.render('Играть заново', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(center=(225, 350))

player_speed = 5
heard_speed = 3 
star_speed=3
meteorid_speed=5
diamond_speed=3

running = True
gameplay = 'start mode'
bg_y = 0
menu_bg_y = 0
score=0
star_score=25
player_x = 150  
player_y = 580  
bullets_left = 25

pygame.mixer.music.load('sounds/sound2.mp3')
pygame.mixer.music.play(-1)

meteorid_timer = pygame.USEREVENT + 1
pygame.time.set_timer(meteorid_timer, 1000)

clock = pygame.time.Clock()

while running:
    keys = pygame.key.get_pressed()
    
    if gameplay=='game':
        screen.blit(bg, (0, bg_y))
        screen.blit(bg, (0, bg_y - 750))
        bg_y += 1
        if bg_y >= 750:
            bg_y = 0
    else:
        screen.blit(bg, (0, menu_bg_y))
        screen.blit(bg, (0, menu_bg_y - 750))
        menu_bg_y += 0.5
        if menu_bg_y >= 750:
            menu_bg_y = 0  
        screen.blit(overlay, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if gameplay=='game':
            if event.type == star_timer:
                star_random_x = random.randint(0, 450 - 30)
                star_rect = star_size.get_rect(topleft=(star_random_x, -30))
                all_stars_in_game.append(star_rect)
            if event.type == meteorid_timer:
                random_size = random.randint(50, 150)
                meteorid = pygame.transform.scale(meteorid_img, (random_size, random_size))
                random_x = random.randint(0, 450 - random_size)
                all_meteorid_in_game.append({
                    "image": meteorid,
                    "rect": meteorid.get_rect(topleft=(random_x, -random_size))
                })
            if event.type == diamond_timer:
                random_x = random.randint(0, 450 - 30)
                star_rect = diamond.get_rect(topleft=(random_x, -30))
                all_diamond_in_game.append(star_rect)
            if event.type == heard_timer:
                heart_random_x = random.randint(0, 450 - 45)
                star_rect = heart.get_rect(topleft=(heart_random_x, -45))
                all_heard_in_game.append(star_rect)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bullets_left != 0:
                    bullet_rect = bullet.get_rect(topleft=(player_x + 80, player_y))
                    bullets.append(bullet_rect)
                    bullets_left -= 1
                    star_score -= 1
                    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if gameplay == 'start mode':
                if restart_label_rect2.collidepoint(event.pos):
                    gameplay = 'dificul mode'
                if close_label_rect.collidepoint(event.pos):
                    running=False
            elif gameplay=='dificul mode':
                if restart_label_rect3.collidepoint(event.pos):
                    player_speed = 5
                    heard_speed = 2
                    star_speed=2
                    meteorid_speed=3
                    diamond_speed=2
                    pteradon_hard = 3
                    gameplay='game'
                if restart_label_rect4.collidepoint(event.pos):
                    player_speed = 3
                    heard_speed = 4
                    star_speed=2
                    meteorid_speed=6
                    diamond_speed=4
                    pteradon_hard = 3
                    gameplay='game'
                if restart_label_rect5.collidepoint(event.pos):
                    player_speed = 2
                    heard_speed = 6
                    star_speed=4
                    meteorid_speed=10
                    diamond_speed=6
                    pteradon_hard = 3
                    gameplay='game'
            elif gameplay == 'game_over': 
                if restart_label_rect.collidepoint(event.pos):
                    gameplay = 'game'
                    player_x = 150
                    player_y = 580
                    score = 0 
                    all_meteorid_in_game.clear()
                    all_heard_in_game.clear()
                    all_stars_in_game.clear()
                    all_diamond_in_game.clear()
                    bullets.clear()
                    bullets_left = 25
                    pteradon_hard = 3
                    star_score = 25

    if gameplay=='start mode':
        screen.blit(restart_label2, restart_label_rect2)
        screen.blit(close_label, close_label_rect)
        all_meteorid_in_game.clear()
        
    elif gameplay=='dificul mode':
        screen.blit(Level_label, Level_label_rect)
        screen.blit(restart_label3, restart_label_rect3)
        screen.blit(restart_label4, restart_label_rect4)
        screen.blit(restart_label5, restart_label_rect5)
        all_meteorid_in_game.clear()
        
    elif gameplay=='game':
        for i in range(pteradon_hard):
            screen.blit(heart, (20 + i * 50, 20))

        screen.blit(diamond, (20, 80))
        screen.blit(player, (player_x, player_y))
        screen.blit(star_size, (20, 130))

        diamond_label = label.render(f'{score}', False, (255, 255, 255))
        screen.blit(diamond_label, (65, 69))
        star_label = label.render(f'{star_score}', False, (255, 255, 255))
        screen.blit(star_label, (65, 115))

        if keys[pygame.K_a] and player_x > 1:
            player_x -= player_speed
        if keys[pygame.K_d] and player_x < 270:
            player_x += player_speed
        if keys[pygame.K_w] and player_y > 350:
            player_y -= player_speed
        if keys[pygame.K_s] and player_y < 570:
            player_y += player_speed

        orig_rect = player.get_rect(topleft=(player_x, player_y))
        player_rect = orig_rect.inflate(-50, -50)
        player_rect.center = orig_rect.center

        if bullets:
            for el in bullets[:]:
                screen.blit(bullet, (el.x, el.y))
                el.y -= 4
                if el.y < 0:
                    bullets.remove(el)
                    
        if all_stars_in_game:
            for star in all_stars_in_game[:]:
                screen.blit(star_size, star)
                star.y += star_speed

                if star.y > 750:
                    all_stars_in_game.remove(star)
                if player_rect.colliderect(star):
                    if bullets_left < 25:
                        star_score += 10
                        bullets_left += 10
                    all_stars_in_game.remove(star)

        if all_meteorid_in_game:
            for el in all_meteorid_in_game[:]: 
                screen.blit(el["image"], el["rect"])
                el["rect"].y += meteorid_speed 

                if el['rect'].y > 750:
                    all_meteorid_in_game.remove(el)

                if player_rect.colliderect(el['rect']):
                    pteradon_hard -= 1
                    all_meteorid_in_game.remove(el)
                    if pteradon_hard <= 0:
                        gameplay = 'game_over'
                        
        if all_heard_in_game:
            for el_heart in all_heard_in_game[:]:
                screen.blit(heart, el_heart)
                el_heart.y += heard_speed 
                if el_heart.y > 750:
                    all_heard_in_game.remove(el_heart)
                if player_rect.colliderect(el_heart):
                    if pteradon_hard < 3:
                        pteradon_hard += 1
                    all_heard_in_game.remove(el_heart)
                    
        if all_diamond_in_game:
            for el_diamond in all_diamond_in_game[:]:
                screen.blit(diamond, el_diamond)
                el_diamond.y += diamond_speed    
                if el_diamond.y > 750:
                    all_diamond_in_game.remove(el_diamond)  
                if player_rect.colliderect(el_diamond):
                    score += 1
                    all_diamond_in_game.remove(el_diamond)
                
        for b in bullets[:]:
            bullet_destroyed = False
            for m in all_meteorid_in_game[:]:
                if b.colliderect(m['rect']):
                    if b in bullets:
                        bullets.remove(b)    
                    if m in all_meteorid_in_game:
                        all_meteorid_in_game.remove(m) 
                    bullet_destroyed = True
                    break            
            if bullet_destroyed:
                continue

    else: 
        screen.blit(lose_label, (100, 150))
        screen.blit(restart_label, restart_label_rect)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
