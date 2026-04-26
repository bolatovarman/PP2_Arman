import pygame
import sys
import json
from db import get_or_create_player, get_connection, save_game_result
from game import SnakeGame

# --- БАПТАУЛАРДЫ БАСҚАРУ ---
def load_settings():
    default_settings = {"snake_color": [0, 255, 0], "grid_overlay": True, "sound_on": True}
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            # Егер файл ішінде керекті кілттер жоқ болса, оларды қосу
            for key, value in default_settings.items():
                if key not in settings:
                    settings[key] = value
            return settings
    except:
        return default_settings

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)

# --- ДЕРЕКТЕР ҚОРЫНАН ДЕРЕКТЕР АЛУ ---
def get_personal_best(player_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id = %s", (player_id,))
    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return res if res else 0

def get_leaderboard():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, s.score, s.level_reached, s.played_at 
        FROM game_sessions s 
        JOIN players p ON s.player_id = p.id 
        ORDER BY s.score DESC LIMIT 10
    """)
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

# --- PYGAME ОРНАТУЛАРЫ ---
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game: TSIS 4")
font = pygame.font.SysFont("Arial", 28)
clock = pygame.time.Clock()

def draw_text(text, x, y, color=(255, 255, 255), center=False):
    img = font.render(str(text), True, color)
    if center:
        x = WIDTH // 2 - img.get_width() // 2
    screen.blit(img, (x, y))

# --- ЭКРАНДАР ---

def settings_screen():
    """Баптаулар экраны: Түс таңдау және торды қосу/өшіру"""
    settings = load_settings()
    colors = [
        ("Green", [0, 255, 0]),
        ("Blue", [0, 0, 255]),
        ("Red", [255, 0, 0]),
        ("Yellow", [255, 255, 0])
    ]
    # Қазіргі түстің индексін табу
    color_idx = 0
    for i, c in enumerate(colors):
        if c[1] == settings["snake_color"]:
            color_idx = i
            break

    while True:
        screen.fill((40, 40, 40))
        draw_text("SETTINGS", 0, 100, (255, 255, 255), center=True)
        
        draw_text(f"C - Snake Color: {colors[color_idx][0]}", 250, 200, colors[color_idx][1])
        draw_text(f"G - Grid Overlay: {'ON' if settings['grid_overlay'] else 'OFF'}", 250, 260)
        draw_text(f"M - Music/Sound: {'ON' if settings['sound_on'] else 'OFF'}", 250, 320)
        
        draw_text("Press S to Save and Back", 0, 450, (150, 150, 150), center=True)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    color_idx = (color_idx + 1) % len(colors)
                    settings["snake_color"] = colors[color_idx][1]
                if event.key == pygame.K_g:
                    settings["grid_overlay"] = not settings["grid_overlay"]
                if event.key == pygame.K_m:
                    settings["sound_on"] = not settings["sound_on"]
                if event.key == pygame.K_s:
                    save_settings(settings)
                    return # Мәзірге қайту

def leaderboard_screen():
    while True:
        screen.fill((20, 20, 20))
        draw_text("TOP 10 LEADERBOARD", 0, 50, (0, 255, 255), center=True)
        leaders = get_leaderboard()
        y_offset = 120
        for i, (name, score, lvl, date) in enumerate(leaders):
            text = f"{i+1}. {name} - {score} pts (Lvl {lvl})"
            draw_text(text, 200, y_offset)
            y_offset += 35
        draw_text("Press B to go Back", 0, 520, (150, 150, 150), center=True)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b: return

def main_menu():
    user_name = ""
    while True:
        screen.fill((30, 30, 30))
        draw_text("SNAKE GAME: TSIS 4", 0, 100, (0, 255, 0), center=True)
        draw_text("Enter your name:", 0, 200, center=True)
        
        input_rect = pygame.Rect(WIDTH//2 - 150, 250, 300, 50)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
        draw_text(user_name, input_rect.x + 10, input_rect.y + 10, (255, 255, 0))
        
        draw_text("ENTER - Play | S - Settings | L - Leaderboard | Q - Quit", 0, 400, (150, 150, 150), center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and user_name.strip():
                    return get_or_create_player(user_name), user_name
                elif event.key == pygame.K_l:
                    leaderboard_screen()
                elif event.key == pygame.K_s:
                    settings_screen()
                elif event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    user_name = user_name[:-1]
                else:
                    if len(user_name) < 12 and event.unicode.isprintable():
                        user_name += event.unicode
        pygame.display.flip()
        clock.tick(30)

def start_game(p_id, p_name):
    settings = load_settings()
    best_score = get_personal_best(p_id)
    game = SnakeGame(screen, settings)
    
    running = True
    while running:
        screen.fill((10, 10, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game.direction != "DOWN": game.direction = "UP"
                if event.key == pygame.K_DOWN and game.direction != "UP": game.direction = "DOWN"
                if event.key == pygame.K_LEFT and game.direction != "RIGHT": game.direction = "LEFT"
                if event.key == pygame.K_RIGHT and game.direction != "LEFT": game.direction = "RIGHT"

        if not game.move():
            save_game_result(p_id, game.score, game.level)
            return game.score, game.level, best_score

        game.draw()
        draw_text(f"Score: {game.score} | Lvl: {game.level}", 20, 20)
        draw_text(f"Best: {best_score}", 20, 50, (100, 255, 100))
        draw_text(p_name, WIDTH - 150, 20, (0, 255, 255))
        
        pygame.display.flip()
        clock.tick(8 + game.level)

def game_over_screen(score, level, best):
    while True:
        screen.fill((50, 0, 0))
        draw_text("GAME OVER", 0, 150, (255, 0, 0), center=True)
        draw_text(f"Score: {score} | Level: {level}", 0, 250, center=True)
        if score > best:
            draw_text("NEW PERSONAL BEST!", 0, 300, (255, 255, 0), center=True)
        
        draw_text("Press R to Retry or M for Menu", 0, 450, (200, 200, 200), center=True)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return "RETRY"
                if event.key == pygame.K_m: return "MENU"

# --- НЕГІЗГІ ЦИКЛ ---
if __name__ == "__main__":
    while True:
        player_id, player_name = main_menu()
        playing = True
        while playing:
            final_score, final_level, best = start_game(player_id, player_name)
            choice = game_over_screen(final_score, final_level, best)
            if choice == "MENU":
                playing = False