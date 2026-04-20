import pygame 
import math
import os
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

try:
    from clock import Clock
except ImportError:
    class Clock:
        def currently_time(self):
            now = datetime.datetime.now()
            return now.minute * 6, now.second * 6

pygame.init()
screen = pygame.display.set_mode((500 , 500))
pygame.display.set_caption("Mickey Clock")

clock = pygame.time.Clock()
logic = Clock()
center = (250 , 250)

try:
    hand_path = os.path.join("images", "hand.png")
    hand_src = pygame.image.load(hand_path).convert_alpha()
except Exception as e:
    pygame.quit()
    exit()

def create_hand(surface, length, width):
    hand_surf = pygame.Surface((length * 2, width * 2), pygame.SRCALPHA)
    scaled_hand = pygame.transform.scale(surface, (length, width))
    hand_surf.blit(scaled_hand, (length, 0))
    return pygame.transform.rotate(hand_surf, 90)

sec_hand_img = create_hand(hand_src, 190, 30) 
min_hand_img = create_hand(hand_src, 140, 50)

def blit_rotate_center(screen, image, center, angle):
    rotated_image = pygame.transform.rotate(image, -angle)
    new_rect = rotated_image.get_rect(center = center)
    screen.blit(rotated_image, new_rect)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    minutes_angles, seconds_angles = logic.currently_time()
    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 0), center, 210, 6)
    for i in range(60):
        angle_rad = math.radians(i * 6 - 90)
        dist = 200
        x1 = center[0] + dist * math.cos(angle_rad)
        y1 = center[1] + dist * math.sin(angle_rad)
        length = 15 if i % 5 == 0 else 7
        width = 3 if i % 5 == 0 else 1
        x2 = center[0] + (dist - length) * math.cos(angle_rad)
        y2 = center[1] + (dist - length) * math.sin(angle_rad)
        pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), width)

    blit_rotate_center(screen, min_hand_img, center, minutes_angles)
    blit_rotate_center(screen, sec_hand_img, center, seconds_angles)
    pygame.draw.circle(screen, (0, 0, 0), center, 10)

    pygame.display.flip()

pygame.quit()