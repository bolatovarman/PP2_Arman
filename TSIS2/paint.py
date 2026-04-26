import pygame
import datetime

# Түстер
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

WIDTH, HEIGHT = 800, 600
FPS = 60

class PaintApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TSIS 2: Advanced Paint Application")
        self.clock = pygame.time.Clock()
        
        # Негізгі канвас
        self.canvas = pygame.Surface((WIDTH, HEIGHT))
        self.canvas.fill(WHITE)
        
        self.running = True
        self.drawing = False
        self.tool = "pencil" 
        self.color = BLACK
        self.thickness = 2
        
        self.start_pos = None
        self.last_pos = None

        # Мәтін құралы үшін айнымалылар
        self.text_font = pygame.font.SysFont("Arial", 24)
        self.active_text = ""
        self.text_pos = None
        self.typing = False

    def save_image(self):
        # 3.4: Сақтау (timestamp арқылы)
        now = datetime.datetime.now()
        filename = f"paint_{now.strftime('%Y%m%d_%H%M%S')}.png"
        pygame.image.save(self.canvas, filename)
        print(f"✅ Сақталды: {filename}")

    def flood_fill(self, x, y, new_color):
        # 3.3: Flood Fill (BFS алгоритмі)
        target_color = self.canvas.get_at((x, y))
        if target_color == new_color: return
        
        queue = [(x, y)]
        while queue:
            curr_x, curr_y = queue.pop(0)
            if not (0 <= curr_x < WIDTH and 0 <= curr_y < HEIGHT): continue
            if self.canvas.get_at((curr_x, curr_y)) != target_color: continue
            
            self.canvas.set_at((curr_x, curr_y), new_color)
            queue.append((curr_x + 1, curr_y))
            queue.append((curr_x - 1, curr_y))
            queue.append((curr_x, curr_y + 1))
            queue.append((curr_x, curr_y - 1))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.typing:
                    if event.key == pygame.K_RETURN:
                        txt_surf = self.text_font.render(self.active_text, True, self.color)
                        self.canvas.blit(txt_surf, self.text_pos)
                        self.typing = False
                    elif event.key == pygame.K_ESCAPE:
                        self.typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.active_text = self.active_text[:-1]
                    else:
                        self.active_text += event.unicode
                    continue

                # Құралдарды пернетақта арқылы таңдау
                if event.key == pygame.K_p: self.tool = "pencil"
                if event.key == pygame.K_l: self.tool = "line"
                if event.key == pygame.K_r: self.tool = "rect"
                if event.key == pygame.K_c: self.tool = "circle"
                if event.key == pygame.K_f: self.tool = "fill"
                if event.key == pygame.K_t: self.tool = "text"
                if event.key == pygame.K_q: self.tool = "square"
                if event.key == pygame.K_v: self.tool = "right_triangle"
                if event.key == pygame.K_e: self.tool = "equilateral_triangle"
                if event.key == pygame.K_b: self.tool = "rhombus"
                
                # 3.2: Өлшемдер (1, 2, 3)
                if event.key == pygame.K_1: self.thickness = 2
                if event.key == pygame.K_2: self.thickness = 5
                if event.key == pygame.K_3: self.thickness = 10
                
                if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self.save_image()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.tool == "fill":
                    self.flood_fill(event.pos[0], event.pos[1], self.color)
                elif self.tool == "text":
                    self.typing = True
                    self.text_pos = event.pos
                    self.active_text = ""
                else:
                    self.drawing = True
                    self.start_pos = event.pos
                    self.last_pos = event.pos
            
            if event.type == pygame.MOUSEBUTTONUP:
                if self.drawing:
                    self.draw_final_shape(event.pos)
                self.drawing = False

            if event.type == pygame.MOUSEMOTION:
                if self.drawing and self.tool == "pencil":
                    pygame.draw.line(self.canvas, self.color, self.last_pos, event.pos, self.thickness)
                    self.last_pos = event.pos

    def get_rect_params(self, start, end):
        x, y = min(start[0], end[0]), min(start[1], end[1])
        w, h = abs(start[0] - end[0]), abs(start[1] - end[1])
        return x, y, w, h

    def draw_final_shape(self, end_pos):
        # Негізгі фигураларды канвасқа салу логикасы
        if self.tool == "line":
            pygame.draw.line(self.canvas, self.color, self.start_pos, end_pos, self.thickness)
        elif self.tool == "rect":
            pygame.draw.rect(self.canvas, self.color, self.get_rect_params(self.start_pos, end_pos), self.thickness)
        elif self.tool == "circle":
            r = int(((self.start_pos[0]-end_pos[0])**2 + (self.start_pos[1]-end_pos[1])**2)**0.5)
            pygame.draw.circle(self.canvas, self.color, self.start_pos, r, self.thickness)
        elif self.tool == "square":
            x, y, w, h = self.get_rect_params(self.start_pos, end_pos)
            side = max(w, h)
            pygame.draw.rect(self.canvas, self.color, (x, y, side, side), self.thickness)
        elif self.tool == "right_triangle":
            pygame.draw.polygon(self.canvas, self.color, [self.start_pos, (self.start_pos[0], end_pos[1]), end_pos], self.thickness)
        elif self.tool == "equilateral_triangle":
            w = end_pos[0] - self.start_pos[0]
            pts = [(self.start_pos[0] + w//2, self.start_pos[1]), (self.start_pos[0], end_pos[1]), (end_pos[0], end_pos[1])]
            pygame.draw.polygon(self.canvas, self.color, pts, self.thickness)
        elif self.tool == "rhombus":
            mx, my = (self.start_pos[0] + end_pos[0]) // 2, (self.start_pos[1] + end_pos[1]) // 2
            pts = [(mx, self.start_pos[1]), (end_pos[0], my), (mx, end_pos[1]), (self.start_pos[0], my)]
            pygame.draw.polygon(self.canvas, self.color, pts, self.thickness)

    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.canvas, (0, 0))
        
        # LIVE PREVIEW
        if self.drawing and self.start_pos:
            curr = pygame.mouse.get_pos()
            if self.tool == "line":
                pygame.draw.line(self.screen, self.color, self.start_pos, curr, self.thickness)
            elif self.tool == "rect":
                pygame.draw.rect(self.screen, self.color, self.get_rect_params(self.start_pos, curr), self.thickness)
            elif self.tool == "circle":
                r = int(((self.start_pos[0]-curr[0])**2 + (self.start_pos[1]-curr[1])**2)**0.5)
                pygame.draw.circle(self.screen, self.color, self.start_pos, r, self.thickness)
            elif self.tool == "square":
                x, y, w, h = self.get_rect_params(self.start_pos, curr)
                side = max(w, h)
                pygame.draw.rect(self.screen, self.color, (x, y, side, side), self.thickness)
            elif self.tool == "rhombus":
                mx, my = (self.start_pos[0] + curr[0]) // 2, (self.start_pos[1] + curr[1]) // 2
                pts = [(mx, self.start_pos[1]), (curr[0], my), (mx, curr[1]), (self.start_pos[0], my)]
                pygame.draw.polygon(self.screen, self.color, pts, self.thickness)
            elif self.tool in ["right_triangle", "equilateral_triangle"]:
                # Үшбұрыштар үшін де preview (жеңілдетілген)
                pygame.draw.line(self.screen, BLUE, self.start_pos, curr, 1)

        if self.typing:
            txt_surf = self.text_font.render(self.active_text + "|", True, RED)
            self.screen.blit(txt_surf, self.text_pos)
        
        self.show_status()
        pygame.display.flip()

    def show_status(self):
        font = pygame.font.SysFont("Arial", 14)
        info = f"Tool: {self.tool.upper()} | Size: {self.thickness} | P, L, R, C, F, T, Q(Sq), V(RT), E(ET), B(Rh) | Ctrl+S"
        self.screen.blit(font.render(info, True, BLACK), (10, 10))

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

if __name__ == "__main__":
    app = PaintApp()
    app.run()