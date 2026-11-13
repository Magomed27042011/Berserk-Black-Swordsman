import pygame
pygame.init()

screen = pygame.display.set_mode((500, 800))
pygame.display.set_caption('Платформер')

player_img = pygame.image.load('icons/player_left/player_left1.png').convert_alpha()
player = pygame.transform.scale(player_img, (50,60))
player_x = 450
player_y = 690
bg_img = pygame.image.load('icons/sky_bg.png').convert_alpha()
bg = pygame.transform.scale(bg_img, (500, 800))
platform_img = pygame.image.load('icons/platform.png')
platform = pygame.transform.scale(platform_img, (180, 120))


clock = pygame.time.Clock()
running = True
while running:
    keys = pygame.key.get_pressed()
    screen.blit(bg, (0, 0))
    screen.blit(player, (player_x,player_y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= 3
    if keys[pygame.K_RIGHT] and player_x < 500 - 50:
        player_x += 3
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()