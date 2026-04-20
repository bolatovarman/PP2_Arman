import pygame
import os

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Music Player")

os.chdir(os.path.dirname(os.path.abspath(__file__)))
songs = [f for f in os.listdir('.') if f.endswith(('.mp3', '.wav'))]
cur = 0

def play():
    if songs:
        try:
            pygame.mixer.music.load(songs[cur])
            pygame.mixer.music.play()
        except:
            pass

if songs: play()
pause = False
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if pause: pygame.mixer.music.unpause()
                else: pygame.mixer.music.pause()
                pause = not pause
            elif event.key == pygame.K_RIGHT:
                cur = (cur + 1) % len(songs)
                play()
            elif event.key == pygame.K_LEFT:
                cur = (cur - 1) % len(songs)
                play()
            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()

    screen.fill((30, 30, 30))
    pygame.display.flip()

pygame.quit()