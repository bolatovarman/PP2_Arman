import pygame
import random

# Константалар
WIDTH, HEIGHT = 400, 600
SPEED = 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Enemy суретін жүктеу
        self.image = pygame.image.load("images/Enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), 0)

    def move(self, score_speed):
        self.rect.move_ip(0, SPEED + score_speed)
        if self.rect.top > HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH-40), 0)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type="oil"):
        super().__init__()
        self.type = type
        if type == "oil":
            self.image = pygame.image.load("images/oil.png").convert_alpha()
        else:
            self.image = pygame.image.load("images/barrier.png").convert_alpha()
        
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), -100)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["nitro", "shield", "repair"])
        
        # Қатеден қорғау: егер фото табылмаса, ойын өшіп қалмайды
        try:
            path = f"images/{self.type}.png"
            self.image = pygame.image.load(path).convert_alpha()
        except FileNotFoundError:
            # Фото табылмаса, жай ғана түрлі-түсті квадрат жасап қоямыз
            self.image = pygame.Surface((30, 30))
            if self.type == "nitro": self.image.fill((0, 255, 0)) # Жасыл
            elif self.type == "shield": self.image.fill((0, 255, 255)) # Көгілдір
            else: self.image.fill((255, 0, 255)) # Қызғылт
            print(f"Ескерту: {self.type}.png файлы 'images/' папкасында табылмады!")

        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), -150)
        self.spawn_time = pygame.time.get_ticks()

    def move(self):
        self.rect.move_ip(0, SPEED)
        # 5 секундтан кейін немесе экраннан кетсе жойылады
        if self.rect.top > HEIGHT or pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT or pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self, weight=1):
        super().__init__()
        self.weight = weight
        # Dollar суретін тиын ретінде қолданамыз
        self.image = pygame.image.load("images/dollar.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH-40), -50)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > HEIGHT:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
        self.base_speed = 7
        self.speed = self.base_speed
        self.has_shield = False
        self.is_nitro = False
        self.nitro_finish = 0

    def move(self):
        if self.is_nitro and pygame.time.get_ticks() > self.nitro_finish:
            self.is_nitro = False
            self.speed = self.base_speed

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(self.speed, 0)

    def apply_powerup(self, p_type):
        if p_type == "nitro":
            self.is_nitro = True
            self.speed = 12
            self.nitro_finish = pygame.time.get_ticks() + 5000
        elif p_type == "shield":
            self.has_shield = True