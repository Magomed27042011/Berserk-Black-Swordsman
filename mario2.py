import pygame
import sys
import random
import math

pygame.init()

# ═══════════════════════════ КОНСТАНТЫ ═══════════════════════════
TILE = 40
ROWS = 15
COLS = 160
WIDTH, HEIGHT = 800, 600
FPS = 60
DT = 1 / FPS
LEVEL_W = COLS * TILE

# Цвета
SKY_TOP = (92, 148, 252)
SKY_BOT = (180, 220, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 205, 60)
RED = (220, 30, 30)
GREEN = (30, 140, 50)
DARK_GREEN = (15, 100, 35)
SKIN = (255, 205, 148)
BROWN = (150, 75, 0)
DARK_BROWN = (95, 55, 20)
BRICK = (196, 110, 52)
DARK_BRICK = (140, 72, 30)
USED = (160, 125, 90)
GRAY = (120, 120, 120)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("СУПЕР МАРИО — Уровень 1-1")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 26)
font_big = pygame.font.SysFont("Arial", 72)
font_med = pygame.font.SysFont("Arial", 40)
font_small = pygame.font.SysFont("Arial", 20)

# ── Звуки (если есть) ─────────────────────────────────────────────
sounds = {}
def init_sounds():
    try:
        pygame.mixer.init()
    except Exception:
        return
    mapping = {
        "jump": "sounds/sound1.mp3",
        "coin": "sounds/sound2.mp3",
        "die": "sounds/sound3.mp3",
    }
    for name, path in mapping.items():
        try:
            sounds[name] = pygame.mixer.Sound(path)
        except Exception:
            pass

def play(name):
    s = sounds.get(name)
    if s:
        try:
            s.play()
        except Exception:
            pass

# ── Спрайт неба ───────────────────────────────────────────────────
sky_surf = pygame.Surface((WIDTH, HEIGHT))
for y in range(HEIGHT):
    t = y / HEIGHT
    col = (
        int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t),
        int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t),
        int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t),
    )
    pygame.draw.line(sky_surf, col, (0, y), (WIDTH, y))

# ── Фон: облака / холмы / кусты ───────────────────────────────────
clouds = []
cx = 0
while cx < LEVEL_W + 400:
    clouds.append((cx + random.randint(0, 200), random.randint(60, 200)))
    cx += random.randint(250, 450)

hills = []
hx = 0
while hx < LEVEL_W + 400:
    hills.append((hx + random.randint(0, 150), random.randint(120, 260)))
    hx += random.randint(350, 600)

def draw_cloud(surf, x, y, s=1.0):
    for dx, dy, r in ((-30, 8, 22), (0, -2, 30), (30, 8, 22), (0, 14, 34)):
        pygame.draw.circle(surf, (255, 255, 255),
                           (int(x + dx * s), int(y + dy * s)), int(r * s))

def draw_hill(surf, x, y):
    pygame.draw.ellipse(surf, (70, 190, 80), pygame.Rect(int(x - y * 1.2), 560 - int(y * 0.82), int(y * 2.4), int(y * 0.9)))

def solid(ch):
    return ch in "X#?U!B[]()|"

# ═══════════════════════════ ИГРОК ═══════════════════════════════
class Player:
    GRAV = 0.5
    JUMP_V = -12.4
    MAX_FALL = 12.0
    MAX_SPEED = 4.8
    ACCEL = 0.5
    FRICTION = 0.82

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w, self.h = 26, 32
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self.facing = 1
        self.walk_t = 0.0
        self.coyote = 0.0
        self.jump_buffer = 0.0
        self.invuln = 0.0
        self.big = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, keys, grid):
        # ── Горизонталь ──
        move = 0
        if keys[pygame.K_LEFT]:
            move -= 1
        if keys[pygame.K_RIGHT]:
            move += 1
        if move != 0:
            self.vx += move * self.ACCEL
            self.vx = max(-self.MAX_SPEED, min(self.MAX_SPEED, self.vx))
            self.facing = move
            self.walk_t += DT
        else:
            self.vx *= self.FRICTION
            if abs(self.vx) < 0.1:
                self.vx = 0

        # ── Прыжок ──
        jump_held = keys[pygame.K_SPACE] or keys[pygame.K_UP]
        if jump_held:
            self.jump_buffer = 0.14
        self.jump_buffer = max(0.0, self.jump_buffer - DT)

        if self.jump_buffer > 0 and (self.on_ground or self.coyote > 0):
            self.vy = self.JUMP_V
            self.on_ground = False
            self.coyote = 0
            self.jump_buffer = 0
            play("jump")

        if not jump_held and self.vy < -4.0:
            self.vy = -4.0

        # ── Гравитация ──
        if self.on_ground:
            self.coyote = 0.09
        else:
            self.coyote = max(0.0, self.coyote - DT)
        self.on_ground = False
        self.vy = min(self.vy + self.GRAV, self.MAX_FALL)

        # ── Коллизии по X ──
        self.x += self.vx
        r = self.rect
        if r.left < 0:
            r.left = 0
        for ty in range(r.top // TILE, (r.bottom - 1) // TILE + 1):
            for tx in range(r.left // TILE, (r.right - 1) // TILE + 1):
                if ty < 0 or ty >= ROWS or tx < 0 or tx >= COLS:
                    continue
                if solid(grid[ty][tx]):
                    if self.vx > 0:
                        r.right = tx * TILE
                    elif self.vx < 0:
                        r.left = (tx + 1) * TILE
                    self.vx = 0
        self.x = r.x

        # ── Коллизии по Y + удар по блокам ──
        self.y += self.vy
        r = self.rect
        bumped = []
        for ty in range(r.top // TILE, (r.bottom - 1) // TILE + 1):
            for tx in range(r.left // TILE, (r.right - 1) // TILE + 1):
                if ty < 0 or ty >= ROWS or tx < 0 or tx >= COLS:
                    continue
                if not solid(grid[ty][tx]):
                    continue
                if self.vy > 0:
                    r.bottom = ty * TILE
                    self.vy = 0
                    self.on_ground = True
                    self.coyote = 0.09
                elif self.vy < 0:
                    r.top = (ty + 1) * TILE
                    self.vy = 0
                    bumped.append((tx, ty))
        self.y = r.y

        if bumped:
            center_x = self.x + self.w / 2
            tx, ty = min(bumped, key=lambda p: (p[1], abs(p[0] * TILE + TILE / 2 - center_x)))
            bump_tile(tx, ty)

        # инвulnerability
        self.invuln = max(0.0, self.invuln - DT)

    def grow(self):
        if not self.big:
            self.big = True
            self.y -= 22
            self.h = 54

    def shrink(self):
        self.big = False
        self.y += 22
        self.h = 32

# ═══════════════════════════ ВРАГИ ═══════════════════════════════
class Goomba:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w, self.h = 30, 30
        self.vx = -0.9
        self.vy = 0.0
        self.squashed = False
        self.t = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, grid):
        if self.squashed:
            self.t -= DT
            return
        dir_sign = 1 if self.vx > 0 else -1
        self.x += self.vx
        r = self.rect

        # стена спереди
        foot_y = r.bottom - 2
        front_x = r.right + 1 if dir_sign > 0 else r.left - 1
        tx = front_x // TILE
        ty = foot_y // TILE
        if 0 <= ty < ROWS and 0 <= tx < COLS and solid(grid[ty][tx]):
            self.vx *= -1

        # край платформы
        below_x = r.right if dir_sign > 0 else r.left
        btx = below_x // TILE
        bty = (r.bottom + 2) // TILE
        if 0 <= bty < ROWS and 0 <= btx < COLS and not solid(grid[bty][btx]):
            self.vx *= -1

        # гравитация и приземление
        self.vy = min(self.vy + 0.5, 12.0)
        self.y += self.vy
        r = self.rect
        for ty in range(r.top // TILE, (r.bottom - 1) // TILE + 1):
            for tx in range(r.left // TILE, (r.right - 1) // TILE + 1):
                if ty < 0 or ty >= ROWS or tx < 0 or tx >= COLS:
                    continue
                if solid(grid[ty][tx]) and self.vy > 0:
                    self.y = ty * TILE - self.h
                    self.vy = 0

    def squash(self):
        self.squashed = True
        self.t = 0.35
        self.h = 12

# ═══════════════════════════ ГРИБ ════════════════════════════════
class Mushroom:
    def __init__(self, bx, by):
        self.x = bx + 6
        self.y = by - 28
        self.w, self.h = 28, 28
        self.vx = 1.4
        self.vy = 0.0
        self.emerge = 0.6

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, grid):
        if self.emerge > 0:
            self.emerge -= DT
            self.y -= 1.2
            return
        self.x += self.vx
        r = self.rect
        for ty in range(r.top // TILE, (r.bottom - 1) // TILE + 1):
            for tx in range(r.left // TILE, (r.right - 1) // TILE + 1):
                if ty < 0 or ty >= ROWS or tx < 0 or tx >= COLS:
                    continue
                if solid(grid[ty][tx]):
                    if self.vx > 0:
                        r.right = tx * TILE
                    elif self.vx < 0:
                        r.left = (tx + 1) * TILE
                    self.vx *= -1
        self.x = r.x
        self.vy = min(self.vy + 0.5, 12.0)
        self.y += self.vy
        r = self.rect
        for ty in range(r.top // TILE, (r.bottom - 1) // TILE + 1):
            for tx in range(r.left // TILE, (r.right - 1) // TILE + 1):
                if ty < 0 or ty >= ROWS or tx < 0 or tx >= COLS:
                    continue
                if solid(grid[ty][tx]) and self.vy > 0:
                    self.y = ty * TILE - self.h
                    self.vy = 0

# ═══════════════════════════ МОНЕТЫ ══════════════════════════════
class CoinPickup:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.phase = random.uniform(0, 6.28)
        self.taken = False

class CoinPop:
    def __init__(self, bx, by):
        self.x = bx + TILE // 2
        self.y = by - 6
        self.vy = -6.5
        self.t = 0.7

    def update(self):
        self.vy += 0.4
        self.y += self.vy
        self.t -= DT

class Particle:
    def __init__(self, bx, by):
        self.x = bx + random.uniform(6, TILE - 6)
        self.y = by + random.uniform(6, TILE - 6)
        self.vx = random.uniform(-2.4, 2.4)
        self.vy = random.uniform(-7.5, -3.5)
        self.t = 1.0
        self.col = random.choice([(225, 150, 60), (150, 75, 20)])

    def update(self):
        self.vy += 0.45
        self.x += self.vx
        self.y += self.vy
        self.t -= DT

# ═══════════════════════════ ГЛОБАЛЬНОЕ СОСТОЯНИЕ ═════════════════
grid = []
player = None
goombas = []
coin_pickups = []
mushrooms = []
pops = []
parts = []

score = 0
coins_count = 0
lives = 3
time_left = 300.0
state = "TITLE"
death_timer = 0.0
clear_timer = 0.0
cleared_shown = False
flag_y = 2 * TILE
anim_t = 0.0
cam_x = 0

FLAG_TILE = 152

def ground_top(tx):
    for ty in range(ROWS):
        if solid(grid[ty][tx]):
            return ty * TILE
    return ROWS * TILE

# ═══════════════════════════ ПОСТРОЕНИЕ УРОВНЯ ════════════════════
def build_level():
    global grid, goombas, coin_pickups, mushrooms, pops, parts, player, flag_y, time_left

    grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
    for x in range(COLS):
        grid[13][x] = "X"
        grid[14][x] = "X"

    def hole(x, w):
        for c in range(x, x + w):
            grid[13][c] = "."
            grid[14][c] = "."

    def pipe(x, h):
        top = 13 - h
        grid[top][x] = "["
        grid[top][x + 1] = "]"
        for r in range(top + 1, 13):
            grid[r][x] = "("
            grid[r][x + 1] = ")"

    def row(y, x, chars):
        for i, ch in enumerate(chars):
            if 0 <= x + i < COLS:
                grid[y][x + i] = ch

    # Ямы
    hole(59, 2)
    hole(97, 2)
    hole(125, 2)
    hole(141, 2)

    # Трубы
    pipe(26, 2)
    pipe(42, 3)
    pipe(88, 2)
    pipe(108, 3)

    # Блоки
    row(9, 12, "?!?")
    row(9, 18, "###")
    row(9, 31, "?")
    row(9, 36, "##")
    row(9, 48, "?#?")
    row(9, 54, "##")
    row(9, 57, "?")
    row(9, 64, "##")
    row(9, 68, "?")
    row(9, 74, "#")
    row(9, 78, "##")
    row(9, 84, "?")
    row(9, 93, "?#")
    row(9, 101, "?#?")
    row(9, 110, "##")
    row(9, 115, "?")
    row(9, 121, "##")
    row(9, 132, "?#?")
    row(9, 137, "##")

    # Высокие блоки
    row(6, 54, "?")
    row(6, 110, "##")
    row(6, 115, "?")
    row(6, 20, "###")
    row(3, 70, "####")

    # Монеты
    row(10, 58, "CCC")
    row(8, 33, "CC")
    row(7, 35, "CC")
    row(6, 56, "CCC")
    row(7, 103, "CC")
    row(5, 113, "CC")
    row(5, 134, "CC")
    row(8, 138, "CC")

    # Враги (обозначение E на строке 12)
    for ex in (5, 9, 16, 22, 33, 39, 46, 51, 61, 67, 73, 81, 92, 105, 112, 118, 131, 136):
        grid[12][ex] = "E"

    # Лестница перед флагом
    for s in range(6):
        for k in range(s + 1):
            grid[13 - k][146 + s] = "X"

    # Собираем сущности
    goombas = []
    coin_pickups = []
    for ty in range(ROWS):
        for tx in range(COLS):
            ch = grid[ty][tx]
            if ch == "E":
                grid[ty][tx] = "."
                gy = ground_top(tx) - 30
                goombas.append(Goomba(tx * TILE + 5, gy))
            elif ch == "C":
                grid[ty][tx] = "."
                coin_pickups.append(CoinPickup(tx * TILE + TILE // 2, ty * TILE + TILE // 2))

    mushrooms = []
    pops = []
    parts = []

    # Игрок
    px = 3 * TILE + 7
    py = ground_top(3) - 32
    player = Player(px, py)

    flag_y = 2 * TILE
    time_left = 300.0

# ═══════════════════════════ ДЕЙСТВИЯ ════════════════════════════
def bump_tile(tx, ty):
    global score
    ch = grid[ty][tx]
    if ch == "?":
        grid[ty][tx] = "U"
        pops.append(CoinPop(tx * TILE, ty * TILE))
        score += 200
        play("coin")
    elif ch == "!":
        grid[ty][tx] = "U"
        mushrooms.append(Mushroom(tx * TILE, ty * TILE))
        play("coin")
    elif ch == "#" and player.big:
        grid[ty][tx] = "."
        for _ in range(4):
            parts.append(Particle(tx * TILE, ty * TILE))
        score += 50
        play("coin")

def add_hud_score(n):
    global score
    score += n

def kill_player():
    global state, death_timer
    state = "DYING"
    death_timer = 2.2
    player.vy = -11.0
    player.vx = 0
    play("die")

def hurt_player():
    if player.big:
        player.shrink()
        player.invuln = 1.8
        player.vy = -6.0
        play("die")
    else:
        kill_player()

def start_game():
    global lives, score, coins_count, state
    lives = 3
    score = 0
    coins_count = 0
    build_level()
    state = "PLAYING"

def reset_level():
    global state
    build_level()
    state = "PLAYING"

def flag_pole_rect():
    x = FLAG_TILE * TILE + TILE // 2 - 3
    return pygame.Rect(x, flag_y, 6, 13 * TILE - flag_y)

# ═══════════════════════════ ОБНОВЛЕНИЕ ═══════════════════════════
def update_playing(keys):
    global state, score, coins_count, time_left, clear_timer, flag_y, cam_x

    player.update(keys, grid)

    for g in goombas:
        g.update(grid)
    for m in mushrooms:
        m.update(grid)
    for p in pops:
        p.update()
    for p in parts:
        p.update()

    pops[:] = [p for p in pops if p.t > 0]
    parts[:] = [p for p in parts if p.t > 0]

    # Сбор монет
    for c in coin_pickups:
        if not c.taken and player.rect.collidepoint(c.x, c.y):
            c.taken = True
            coins_count += 1
            score += 200
            play("coin")
    coin_pickups[:] = [c for c in coin_pickups if not c.taken]

    # Враги
    for g in goombas[:]:
        if g.squashed:
            if g.t <= 0:
                goombas.remove(g)
            continue
        if player.rect.colliderect(g.rect):
            if player.vy > 0 and player.rect.bottom - g.rect.centery < 16:
                g.squash()
                score += 100
                player.vy = -7.5
                play("coin")
            elif player.invuln <= 0:
                hurt_player()
                break

    # Грибы
    for m in mushrooms[:]:
        if player.rect.colliderect(m.rect):
            if not player.big:
                player.grow()
            score += 1000
            mushrooms.remove(m)
            play("coin")

    # Флаг
    if player.rect.colliderect(flag_pole_rect()):
        state = "LEVEL_CLEAR"
        clear_timer = 0.0
        cleared_shown = False
        player.vx = 0
        play("die")

    # Яма
    if player.y > ROWS * TILE:
        kill_player()
        return

    # Время
    time_left -= DT
    if time_left <= 0:
        kill_player()
        return

    # Камера
    cam = int(player.x + player.w / 2 - WIDTH / 2)
    cam_x = max(0, min(cam, LEVEL_W - WIDTH))

def update_dying():
    global state, death_timer, lives
    death_timer -= DT
    player.vy = min(player.vy + 0.5, 12.0)
    player.y += player.vy
    if death_timer <= 0:
        lives -= 1
        if lives > 0:
            reset_level()
        else:
            state = "GAME_OVER"

def update_clear():
    global clear_timer, flag_y, cleared_shown
    clear_timer += DT
    if flag_y < 13 * TILE - 20:
        flag_y += 3.0
    if clear_timer > 2.2:
        cleared_shown = True

# ═══════════════════════════ ОТРИСОВКА ═══════════════════════════
def draw_background():
    screen.blit(sky_surf, (0, 0))
    for c in clouds:
        sx = c[0] - cam_x * 0.3
        if -80 <= sx <= WIDTH + 80:
            draw_cloud(screen, int(sx), c[1])
    for h in hills:
        sx = h[0] - cam_x * 0.5
        if -260 <= sx <= WIDTH + 260:
            draw_hill(screen, int(sx), h[1])

def draw_ground_tile(sx, sy, ty):
    pygame.draw.rect(screen, BRICK, (sx, sy, TILE, TILE))
    pygame.draw.rect(screen, DARK_BRICK, (sx, sy, TILE, TILE), 2)
    # горизонтальный шов
    pygame.draw.line(screen, DARK_BRICK, (sx, sy + TILE // 2), (sx + TILE, sy + TILE // 2), 2)
    # вертикальные швы (в шахматном порядке)
    off = TILE // 2 if (tx_parity(sx) == 1) else 0
    pygame.draw.line(screen, DARK_BRICK, (sx + TILE // 2, sy + off), (sx + TILE // 2, sy + TILE // 2), 2)
    if ty == 13:
        pygame.draw.rect(screen, (215, 140, 70), (sx, sy, TILE, 8))
        pygame.draw.line(screen, DARK_BRICK, (sx, sy + 8), (sx + TILE, sy + 8), 2)

def tx_parity(sx):
    return (sx // TILE) % 2

def draw_brick(sx, sy):
    pygame.draw.rect(screen, BRICK, (sx, sy, TILE, TILE))
    pygame.draw.rect(screen, DARK_BRICK, (sx, sy, TILE, TILE), 2)
    pygame.draw.line(screen, DARK_BRICK, (sx, sy + TILE // 2), (sx + TILE, sy + TILE // 2), 2)
    pygame.draw.line(screen, DARK_BRICK, (sx + TILE // 2, sy), (sx + TILE // 2, sy + TILE // 2), 2)

def draw_question(sx, sy, mush=False):
    pulse = int(10 * math.sin(anim_t * 3))
    base = (255, 195 + pulse, 40)
    pygame.draw.rect(screen, base, (sx, sy, TILE, TILE))
    pygame.draw.rect(screen, (120, 70, 10), (sx, sy, TILE, TILE), 3)
    pygame.draw.rect(screen, (255, 240, 150), (sx + 3, sy + 3, TILE - 6, TILE - 6), 2)
    # заклёпки
    for rx, ry in ((6, 6), (TILE - 10, 6), (6, TILE - 10), (TILE - 10, TILE - 10)):
        pygame.draw.rect(screen, (120, 70, 10), (sx + rx, sy + ry, 4, 4))
    txt = font_med.render("M" if mush else "?", True, WHITE)
    screen.blit(txt, txt.get_rect(center=(sx + TILE // 2, sy + TILE // 2 - 2)))

def draw_used(sx, sy):
    pygame.draw.rect(screen, USED, (sx, sy, TILE, TILE))
    pygame.draw.rect(screen, DARK_BROWN, (sx, sy, TILE, TILE), 3)
    for rx, ry in ((6, 6), (TILE - 10, 6), (6, TILE - 10), (TILE - 10, TILE - 10)):
        pygame.draw.rect(screen, DARK_BROWN, (sx + rx, sy + ry, 4, 4))

def draw_pipe(sx, sy, ch):
    light = (60, 200, 80)
    dark = (10, 90, 30)
    pygame.draw.rect(screen, dark, (sx, sy, TILE, TILE))
    pygame.draw.rect(screen, light, (sx + 2, sy + 2, TILE - 4, TILE - 4))
    pygame.draw.rect(screen, (160, 255, 170), (sx + 5, sy + 3, 6, TILE - 6))
    if ch == "[":
        pygame.draw.rect(screen, dark, (sx - 3, sy - 3, TILE + 6, 8))
        pygame.draw.rect(screen, light, (sx - 1, sy - 2, TILE + 2, 5))
    elif ch == "]":
        pygame.draw.rect(screen, dark, (sx - 3, sy - 3, TILE + 6, 8))
        pygame.draw.rect(screen, light, (sx - 1, sy - 2, TILE + 2, 5))

def draw_tiles():
    start_col = max(0, cam_x // TILE - 1)
    end_col = min(COLS, start_col + WIDTH // TILE + 2)
    for ty in range(ROWS):
        for tx in range(start_col, end_col):
            ch = grid[ty][tx]
            if ch == ".":
                continue
            sx = tx * TILE - cam_x
            sy = ty * TILE
            if ch == "X":
                draw_ground_tile(sx, sy, ty)
            elif ch == "#":
                draw_brick(sx, sy)
            elif ch == "?":
                draw_question(sx, sy)
            elif ch == "!":
                draw_question(sx, sy, mush=True)
            elif ch == "U":
                draw_used(sx, sy)
            elif ch in "[ ] ( )".split():
                draw_pipe(sx, sy, ch)

def draw_coin(x, y, phase, scale=1.0):
    w = max(4, int(14 * abs(math.cos(phase))) )
    pygame.draw.ellipse(screen, (255, 200, 40), pygame.Rect(int(x - w / 2), int(y - 10), w, 20))
    pygame.draw.ellipse(screen, (255, 240, 120), pygame.Rect(int(x - w / 2 + 2), int(y - 8), max(2, w - 4), 16))
    pygame.draw.ellipse(screen, YELLOW, pygame.Rect(int(x - w / 2 + 4), int(y - 6), max(2, w - 8), 12))

def draw_mario(x, y, facing, frame, big, alpha=255):
    w, h = (26, 32) if not big else (26, 54)
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    skin = (255, 205, 148)
    red = (220, 40, 30)
    blue = (40, 60, 200)
    brown2 = (110, 60, 20)

    if not big:
        # кепка
        pygame.draw.rect(surf, red, (6, 0, 14, 5))
        pygame.draw.rect(surf, red, (3, 4, 20, 3))
        # лицо
        pygame.draw.rect(surf, skin, (7, 5, 12, 9))
        # глаза
        pygame.draw.rect(surf, BLACK, (10, 7, 2, 3))
        pygame.draw.rect(surf, BLACK, (15, 7, 2, 3))
        # усы
        pygame.draw.rect(surf, (60, 30, 10), (12, 9, 5, 2))
        # рубашка
        pygame.draw.rect(surf, red, (5, 14, 16, 7))
        # руки
        pygame.draw.rect(surf, red, (2, 14, 4, 7))
        pygame.draw.rect(surf, red, (20, 14, 4, 7))
        # комбинезон
        pygame.draw.rect(surf, blue, (5, 19, 16, 8))
        # лямки
        pygame.draw.rect(surf, blue, (7, 17, 3, 5))
        pygame.draw.rect(surf, blue, (16, 17, 3, 5))
        pygame.draw.rect(surf, YELLOW, (8, 21, 2, 2))
        pygame.draw.rect(surf, YELLOW, (16, 21, 2, 2))
        # ноги (шаг)
        leg = 3 if frame else 0
        pygame.draw.rect(surf, brown2, (5, 25 + leg, 8, 7 - leg))
        pygame.draw.rect(surf, brown2, (13, 25 - leg, 8, 7 + leg))
    else:
        # кепка
        pygame.draw.rect(surf, red, (6, 0, 14, 7))
        pygame.draw.rect(surf, red, (3, 6, 20, 4))
        # лицо
        pygame.draw.rect(surf, skin, (7, 8, 12, 13))
        # глаза
        pygame.draw.rect(surf, BLACK, (10, 10, 2, 4))
        pygame.draw.rect(surf, BLACK, (15, 10, 2, 4))
        pygame.draw.rect(surf, (60, 30, 10), (12, 14, 6, 3))
        # рубашка
        pygame.draw.rect(surf, red, (5, 20, 16, 12))
        pygame.draw.rect(surf, red, (1, 20, 5, 12))
        pygame.draw.rect(surf, red, (20, 20, 5, 12))
        # комбинезон
        pygame.draw.rect(surf, blue, (4, 30, 18, 14))
        pygame.draw.rect(surf, blue, (6, 26, 4, 8))
        pygame.draw.rect(surf, blue, (16, 26, 4, 8))
        pygame.draw.rect(surf, YELLOW, (8, 32, 3, 3))
        pygame.draw.rect(surf, YELLOW, (15, 32, 3, 3))
        # ноги
        leg = 4 if frame else 0
        pygame.draw.rect(surf, brown2, (4, 42 + leg, 9, 12 - leg))
        pygame.draw.rect(surf, brown2, (13, 42 - leg, 9, 12 + leg))

    if facing < 0:
        surf = pygame.transform.flip(surf, True, False)
    if alpha < 255:
        surf.set_alpha(alpha)
    screen.blit(surf, (int(x), int(y)))

def draw_goomba(g):
    x, y = int(g.x), int(g.y)
    if g.squashed:
        pygame.draw.rect(screen, BROWN, (x, y, g.w, g.h))
        pygame.draw.rect(screen, DARK_BROWN, (x, y, g.w, g.h), 2)
        return
    # ноги
    pygame.draw.rect(screen, (225, 200, 160), (x + 3, y + 24, 11, 6))
    pygame.draw.rect(screen, (225, 200, 160), (x + 16, y + 24, 11, 6))
    # тело
    pygame.draw.ellipse(screen, BROWN, (x + 1, y + 8, 28, 18))
    pygame.draw.ellipse(screen, BROWN, (x + 1, y + 2, 28, 20))
    pygame.draw.ellipse(screen, DARK_BROWN, (x + 1, y + 2, 28, 20), 2)
    # брови
    pygame.draw.rect(screen, (50, 25, 10), (x + 5, y + 8, 9, 3))
    pygame.draw.rect(screen, (50, 25, 10), (x + 16, y + 8, 9, 3))
    # глаза
    pygame.draw.rect(screen, WHITE, (x + 7, y + 11, 6, 6))
    pygame.draw.rect(screen, WHITE, (x + 17, y + 11, 6, 6))
    pygame.draw.rect(screen, BLACK, (x + 9, y + 13, 3, 3))
    pygame.draw.rect(screen, BLACK, (x + 19, y + 13, 3, 3))

def draw_mushroom(m):
    x, y = int(m.x), int(m.y)
    # ножка
    pygame.draw.rect(screen, (245, 230, 200), (x + 7, y + 14, 14, 14))
    # пятна
    pygame.draw.circle(screen, WHITE, (x + 8, y + 6), 4)
    pygame.draw.circle(screen, WHITE, (x + 19, y + 9), 3)
    # шляпка
    pygame.draw.ellipse(screen, RED, (x, y + 2, 28, 16))
    pygame.draw.ellipse(screen, (120, 10, 10), (x, y + 16, 28, 4))
    # глазки
    if m.emerge <= 0:
        pygame.draw.rect(screen, BLACK, (x + 8, y + 18, 3, 4))
        pygame.draw.rect(screen, BLACK, (x + 17, y + 18, 3, 4))

def draw_flag():
    px = FLAG_TILE * TILE + TILE // 2
    # шест
    pygame.draw.line(screen, (60, 180, 90), (px, int(flag_y)), (px, 13 * TILE), 5)
    # шар
    pygame.draw.circle(screen, (255, 210, 60), (px, int(flag_y)), 8)
    # флаг
    fy = int(flag_y)
    pygame.draw.polygon(screen, RED, [(px - 2, fy + 4), (px - 44, fy + 18), (px - 2, fy + 32)])
    pygame.draw.circle(screen, WHITE, (px - 18, fy + 18), 5)

def draw_hud():
    strip = pygame.Surface((WIDTH, 44), pygame.SRCALPHA)
    strip.fill((0, 0, 0, 150))
    screen.blit(strip, (0, 0))
    left = 16
    texts = [
        f"СЧЁТ {score:06d}",
        f"МОНЕТЫ {coins_count:02d}",
        f"МИР 1-1",
        f"ВРЕМЯ {max(0, int(time_left))}",
    ]
    for t in texts:
        surf = font.render(t, True, WHITE)
        screen.blit(surf, (left, 8))
        left += surf.get_width() + 40
    # жизни
    lives_txt = font.render(f"ЖИЗНИ {lives}", True, (255, 120, 120))
    screen.blit(lives_txt, (WIDTH - lives_txt.get_width() - 16, 8))

def draw_world():
    draw_background()
    draw_tiles()

    # монеты
    for c in coin_pickups:
        draw_coin(c.x, c.y, c.phase)
        c.phase += 0.12

    # грибы
    for m in mushrooms:
        draw_mushroom(m)

    # отрисовка флага ПОЗАДИ игрока но поверх труб? — шест над землёй
    draw_flag()

    # враги
    for g in goombas:
        draw_goomba(g)

    # частицы и монеты-поп
    for p in parts:
        pygame.draw.rect(screen, p.col, (int(p.x), int(p.y), 6, 6))
    for p in pops:
        draw_coin(p.x, p.y, 0)

    # игрок
    if player:
        flicker = player.invuln > 0 and int(player.invuln * 12) % 2 == 0
        if not flicker:
            frame = int(player.walk_t * 7) % 2
            draw_mario(player.x, player.y, player.facing, frame, player.big)

    draw_hud()

def draw_title():
    screen.blit(sky_surf, (0, 0))
    for c in clouds:
        draw_cloud(screen, c[0] % WIDTH, c[1])
    # земля
    for tx in range(WIDTH // TILE + 1):
        draw_ground_tile(tx * TILE, 13 * TILE, 13)
        draw_ground_tile(tx * TILE, 14 * TILE, 14)

    title = font_big.render("СУПЕР МАРИО", True, (255, 210, 40))
    shadow = font_big.render("СУПЕР МАРИО", True, (150, 20, 10))
    screen.blit(shadow, title.get_rect(center=(WIDTH // 2 + 5, 185)))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

    sub = font_med.render("УРОВЕНЬ 1-1", True, WHITE)
    screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 260)))

    # персонажи
    draw_mario(WIDTH // 2 - 80, 420, 1, 0, False)
    draw_mario(WIDTH // 2 - 30, 400, 1, 0, True)
    draw_goomba(Goomba(WIDTH // 2 + 60, 13 * TILE - 30))

    hint1 = font.render("СТРЕЛКИ — движение      ПРОБЕЛ/ВВЕРХ — прыжок", True, (235, 235, 235))
    hint2 = font.render("Найди флаг в конце уровня! Избегай гумб и ям.", True, (235, 235, 235))
    screen.blit(hint1, hint1.get_rect(center=(WIDTH // 2, 500)))
    screen.blit(hint2, hint2.get_rect(center=(WIDTH // 2, 535)))

    go = font_med.render("НАЖМИ ENTER", True, YELLOW)
    rect = go.get_rect(center=(WIDTH // 2, 340))
    pygame.draw.rect(screen, (0, 0, 0, 0), rect)
    screen.blit(go, rect)

def draw_game_over():
    screen.fill((20, 10, 10))
    t = font_big.render("ИГРА ОКОНЧЕНА", True, RED)
    screen.blit(t, t.get_rect(center=(WIDTH // 2, 250)))
    s = font.render(f"СЧЁТ: {score}     МОНЕТЫ: {coins_count}", True, WHITE)
    screen.blit(s, s.get_rect(center=(WIDTH // 2, 320)))
    g = font_med.render("НАЖМИ ENTER", True, YELLOW)
    screen.blit(g, g.get_rect(center=(WIDTH // 2, 380)))

def draw_level_clear():
    screen.blit(sky_surf, (0, 0))
    draw_world()
    if cleared_shown:
        t = font_big.render("УРОВЕНЬ ПРОЙДЕН!", True, (255, 210, 40))
        shadow = font_big.render("УРОВЕНЬ ПРОЙДЕН!", True, (150, 20, 10))
        screen.blit(shadow, t.get_rect(center=(WIDTH // 2 + 4, 240)))
        screen.blit(t, t.get_rect(center=(WIDTH // 2, 235)))
        s = font_med.render(f"СЧЁТ: {score}", True, WHITE)
        screen.blit(s, s.get_rect(center=(WIDTH // 2, 320)))
        g = font.render("НАЖМИ ENTER", True, YELLOW)
        screen.blit(g, g.get_rect(center=(WIDTH // 2, 370)))

# ═══════════════════════════ ГЛАВНЫЙ ЦИКЛ ═════════════════════════
def main():
    global state, anim_t
    init_sounds()
    build_level()
    state = "TITLE"
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if state == "TITLE" and event.key == pygame.K_RETURN:
                    start_game()
                elif state == "GAME_OVER" and event.key == pygame.K_RETURN:
                    state = "TITLE"
                elif state == "LEVEL_CLEAR" and cleared_shown and event.key == pygame.K_RETURN:
                    state = "TITLE"

        keys = pygame.key.get_pressed()
        anim_t += DT

        if state == "PLAYING":
            update_playing(keys)
        elif state == "DYING":
            update_dying()
        elif state == "LEVEL_CLEAR":
            update_clear()

        if state == "TITLE":
            draw_title()
        elif state == "PLAYING":
            draw_world()
        elif state == "DYING":
            draw_world()
        elif state == "LEVEL_CLEAR":
            draw_level_clear()
        elif state == "GAME_OVER":
            draw_game_over()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()