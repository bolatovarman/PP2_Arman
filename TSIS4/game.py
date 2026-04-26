import pygame
import random

# Константалар
BLOCK_SIZE = 20

class SnakeGame:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.width, self.height = screen.get_size()
        
        # Жыланның бастапқы күйі
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.direction = "RIGHT"
        self.score = 0
        self.level = 1
        
        # Кедергілер (Obstacles)
        self.obstacles = []
        self.update_obstacles() 
        
        # Тамақтар
        self.food = self.spawn_item()
        self.poison = self.spawn_item()
        
        # Бонустар (Power-ups)
        self.powerup = None
        self.powerup_time = 0

    def spawn_item(self):
        """Экранда кездейсоқ бос орын табу"""
        while True:
            x = random.randrange(0, self.width, BLOCK_SIZE)
            y = random.randrange(0, self.height, BLOCK_SIZE)
            pos = [x, y]
            if pos not in self.snake and pos not in self.obstacles:
                return pos

    def update_obstacles(self):
        """3-деңгейден бастап кедергілерді құру"""
        self.obstacles = []
        if self.level >= 3:
            for _ in range(self.level * 2):
                obs = self.spawn_item()
                self.obstacles.append(obs)

    def move(self):
        """Жыланның қозғалысы және логикасы"""
        head = self.snake[0].copy()

        # Бағытты анықтау
        if self.direction == "UP": head[1] -= BLOCK_SIZE
        elif self.direction == "DOWN": head[1] += BLOCK_SIZE
        elif self.direction == "LEFT": head[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT": head[0] += BLOCK_SIZE
        
        # 1. Бонус (Power-up) пайда болу логикасы
        # Ұпай 50-ге еселенгенде және экранда бонус жоқ болса
        if self.score > 0 and self.score % 50 == 0 and not self.powerup:
            self.powerup = self.spawn_item()
            self.powerup_time = pygame.time.get_ticks()

        # Бонусты жеу немесе жоғалып кетуі
        if self.powerup:
            if head == self.powerup:
                self.score += 50
                self.powerup = None
            elif pygame.time.get_ticks() - self.powerup_time > 5000: # 5 секунд
                self.powerup = None

        # Жаңа басты қосу
        self.snake.insert(0, head)

        # 2. Тамақ жеу
        if head == self.food:
            self.score += 10
            self.food = self.spawn_item()
            old_level = self.level
            self.level = (self.score // 30) + 1
            if self.level != old_level:
                self.update_obstacles()
        else:
            self.snake.pop()

        # 3. Улы тамақ жеу (Poison)
        if head == self.poison:
            self.poison = self.spawn_item()
            if len(self.snake) > 2:
                self.snake.pop()
            else:
                return False

        # 4. Соқтығысуларды тексеру
        if (head[0] < 0 or head[0] >= self.width or 
            head[1] < 0 or head[1] >= self.height or 
            head in self.snake[1:] or 
            head in self.obstacles):
            return False
            
        return True

    def draw(self):
        """Экранға барлық элементтерді салу"""
        # 1. Торды салу
        if self.settings.get("grid_overlay", True):
            for x in range(0, self.width, BLOCK_SIZE):
                pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, self.height))
            for y in range(0, self.height, BLOCK_SIZE):
                pygame.draw.line(self.screen, (30, 30, 30), (0, y), (self.width, y))

        # 2. Жыланды салу
        snake_color = self.settings.get("snake_color", [0, 255, 0])
        for segment in self.snake:
            pygame.draw.rect(self.screen, snake_color, (segment[0], segment[1], BLOCK_SIZE - 2, BLOCK_SIZE - 2))
        
        # 3. Тамақтар мен Бонусты салу
        # Кәдімгі тамақ (Қызыл)
        pygame.draw.rect(self.screen, (255, 0, 0), (self.food[0], self.food[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Улы тамақ (Күңгірт қызыл)
        pygame.draw.rect(self.screen, (150, 0, 0), (self.poison[0], self.poison[1], BLOCK_SIZE, BLOCK_SIZE))
        
        # Бонус (Алтын шеңбер)
        if self.powerup:
            pygame.draw.circle(self.screen, (255, 215, 0), (self.powerup[0] + 10, self.powerup[1] + 10), 10)
        
        # 4. Кедергілерді салу (Сұр)
        for obs in self.obstacles:
            pygame.draw.rect(self.screen, (100, 100, 100), (obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))