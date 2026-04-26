import pygame
import sys
import random
from racer import Player, Enemy, Coin, Obstacle, PowerUp
from persistence import load_settings, save_settings, load_leaderboard, save_score

# Түстер
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 400, 600
FPS = 60

class RacerGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Racer: Advanced Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28)
        
        # Баптаулар мен Фонды жүктеу
        self.settings = load_settings()
        try:
            self.bg = pygame.image.load("images/AnimatedStreet.png").convert()
            self.bg = pygame.transform.scale(self.bg, (WIDTH, HEIGHT))
        except:
            self.bg = pygame.Surface((WIDTH, HEIGHT))
            self.bg.fill((50, 50, 50))
            
        self.bg_y = 0
        self.user_name = ""
        self.state = "MENU" 
        self.running = True
        self.state_reset = True

    def draw_text(self, text, x, y, color=BLACK):
        img = self.font.render(text, True, color)
        self.screen.blit(img, (x, y))

    def reset_game(self):
        self.player = Player()
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy())
        self.coins = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.enemies)
        
        self.score = 0
        self.coin_count = 0
        self.speed_bonus = 0

    def main_menu(self):
        self.screen.fill(WHITE)
        self.draw_text("RACER GAME", 110, 80, RED)
        
        buttons = [
            (pygame.Rect(100, 180, 200, 50), "PLAY", "USERNAME"),
            (pygame.Rect(100, 250, 200, 50), "SCORES", "LEADERBOARD"),
            (pygame.Rect(100, 320, 200, 50), "SETTINGS", "SETTINGS"),
            (pygame.Rect(100, 390, 200, 50), "QUIT", "QUIT")
        ]

        for rect, text, state in buttons:
            pygame.draw.rect(self.screen, GRAY, rect)
            self.draw_text(text, rect.x + 50, rect.y + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, text, state in buttons:
                    if rect.collidepoint(event.pos):
                        if state == "QUIT": self.running = False
                        else: self.state = state

    def username_screen(self):
        self.screen.fill(WHITE)
        self.draw_text("ENTER YOUR NAME:", 85, 200, BLACK)
        pygame.draw.line(self.screen, BLACK, (100, 300), (300, 300), 2)
        name_img = self.font.render(self.user_name + "|", True, BLUE)
        self.screen.blit(name_img, (110, 265))
        self.draw_text("Press ENTER to Start", 85, 400, GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if not self.user_name.strip(): self.user_name = "Player1"
                    self.state = "GAME"
                elif event.key == pygame.K_BACKSPACE:
                    self.user_name = self.user_name[:-1]
                else:
                    if len(self.user_name) < 10: self.user_name += event.unicode

    def settings_screen(self):
        self.screen.fill(WHITE)
        self.draw_text("SETTINGS", 140, 50, RED)
        
        # Дыбыс пен Қиындық батырмалары
        sound_text = f"Sound: {'ON' if self.settings['sound_on'] else 'OFF'}"
        sound_rect = pygame.Rect(100, 150, 200, 50)
        pygame.draw.rect(self.screen, GRAY, sound_rect)
        self.draw_text(sound_text, 120, 160)

        diff_rect = pygame.Rect(100, 230, 200, 50)
        pygame.draw.rect(self.screen, GRAY, diff_rect)
        self.draw_text(f"Diff: {self.settings['difficulty']}", 120, 240)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sound_rect.collidepoint(event.pos):
                    self.settings['sound_on'] = not self.settings['sound_on']
                if diff_rect.collidepoint(event.pos):
                    levels = ["Easy", "Medium", "Hard"]
                    idx = (levels.index(self.settings['difficulty']) + 1) % 3
                    self.settings['difficulty'] = levels[idx]
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                save_settings(self.settings)
                self.state = "MENU"

    def leaderboard_screen(self):
        self.screen.fill(WHITE)
        self.draw_text("TOP 10 SCORES", 100, 50, RED)
        scores = load_leaderboard()
        for i, entry in enumerate(scores):
            self.draw_text(f"{i+1}. {entry['name']}: {entry['score']}", 80, 120 + (i * 35))
        self.draw_text("Press ESC to Back", 100, 530, GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: self.state = "MENU"

    def game_over_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 120, 200, RED)
        self.draw_text(f"Final Score: {self.score}", 110, 260, WHITE)
        self.draw_text("Press ENTER to Menu", 80, 350, GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = "MENU"
                self.state_reset = True

    def game_loop(self):
        if self.state_reset:
            self.reset_game()
            self.state_reset = False

        # Анимацияланған фон
        self.screen.blit(self.bg, (0, self.bg_y))
        self.screen.blit(self.bg, (0, self.bg_y - HEIGHT))
        self.bg_y += 5
        if self.bg_y >= HEIGHT: self.bg_y = 0
        
        # Спаун (Тиын, Кедергі, Бонус)
        if random.randint(1, 120) < 2:
            c = Coin(); self.coins.add(c); self.all_sprites.add(c)
        if random.randint(1, 180) < 2:
            o = Obstacle(type=random.choice(["oil", "barrier"])); self.obstacles.add(o); self.all_sprites.add(o)
        if random.randint(1, 400) < 2:
            p = PowerUp(); self.powerups.add(p); self.all_sprites.add(p)

        # Қозғалыс
        self.player.move()
        for e in self.enemies: e.move(self.speed_bonus)
        for s in self.coins: s.move()
        for s in self.obstacles: s.move()
        for s in self.powerups: s.move()

        # Соқтығысу логикасы
        if pygame.sprite.spritecollide(self.player, self.coins, True):
            self.coin_count += 1
            self.score += 10
            self.speed_bonus = self.coin_count // 5

        p_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for p in p_hits:
            if p.type == "repair": self.score += 100
            else: self.player.apply_powerup(p.type)

        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.player.rect.move_ip(random.randint(-8, 8), 0)

        if pygame.sprite.spritecollide(self.player, self.enemies, False):
            if self.player.has_shield:
                self.player.has_shield = False
                for e in self.enemies: e.rect.top = -100
            else:
                save_score(self.user_name, self.score)
                self.state = "GAMEOVER"

        # Сурет салу
        for s in self.all_sprites: self.screen.blit(s.image, s.rect)
        for s in self.enemies: self.screen.blit(s.image, s.rect)
        
        # UI
        self.draw_text(f"Score: {self.score}", 10, 10, YELLOW)
        self.draw_text(f"Name: {self.user_name}", 250, 10, WHITE)
        if self.player.has_shield: self.draw_text("SHIELD ACTIVE", 10, 40, BLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state = "MENU"; self.state_reset = True

    def run(self):
        while self.running:
            if self.state == "MENU": self.main_menu()
            elif self.state == "USERNAME": self.username_screen()
            elif self.state == "GAME": self.game_loop()
            elif self.state == "SETTINGS": self.settings_screen()
            elif self.state == "LEADERBOARD": self.leaderboard_screen()
            elif self.state == "GAMEOVER": self.game_over_screen()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    game = RacerGame()
    game.run()