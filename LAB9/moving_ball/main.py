import pygame
from ball import Ball

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("moving ball")

clock = pygame.time.Clock()

ball = Ball()

running = True
while running:
    clock.tick(120)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                ball.move_left()
            if event.key == pygame.K_RIGHT:
                ball.move_right()
            if event.key == pygame.K_UP:
                ball.move_up()
            if event.key == pygame.K_DOWN:
                ball.move_down()

    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (255, 0, 0), (ball.x, ball.y), ball.r)

    pygame.display.flip()

pygame.quit()
