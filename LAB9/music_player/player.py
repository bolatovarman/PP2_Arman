import pygame

class Player:
    def __init__(self, music_file):
        self.music_file = music_file

    def play_music(self):
        pygame.mixer.music.load(self.music_file)
        pygame.mixer.music.play()

    def stop_music(self):
        pygame.mixer.music.stop()
