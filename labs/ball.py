import pygame

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Move the Ball")

ball_radius = 25
ball_color = (255, 0, 0)
ball_x = width // 2
ball_y = height // 2

move_distance = 20

background_color = (255, 255, 255)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if ball_y - ball_radius - move_distance >= 0: 
            ball_y -= move_distance
    if keys[pygame.K_DOWN]:
        if ball_y + ball_radius + move_distance <= height:
            ball_y += move_distance
    if keys[pygame.K_LEFT]:
        if ball_x - ball_radius - move_distance >= 0:
            ball_x -= move_distance
    if keys[pygame.K_RIGHT]:
        if ball_x + ball_radius + move_distance <= width: 
            ball_x += move_distance

    screen.fill(background_color)

    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
