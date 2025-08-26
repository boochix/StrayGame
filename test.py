import pygame
import random
import sys

# --- CONFIG ---
GRID_SIZE = 8            # 8x8 grid
TILE_SIZE = 64           # pixels per tile
WINDOW_SIZE = GRID_SIZE * TILE_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (100, 200, 100)
RED = (200, 100, 100)
GRAY = (200, 200, 200)
BLUE = (100, 100, 255)

# --- GAME STATE ---
lives = 4
stage = 1
dog_pos = [0, 0]  # start top-left
danger_tiles = set()

pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 50))
pygame.display.set_caption("Stray Dog Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# --- FUNCTIONS ---
def generate_danger_tiles(stage):
    """Generate danger tiles based on stage difficulty."""
    num_danger = stage * 5  # scale difficulty
    tiles = set()
    while len(tiles) < num_danger:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if [x, y] != dog_pos and (x, y) != (GRID_SIZE-1, GRID_SIZE-1):
            tiles.add((x, y))
    return tiles

def draw_grid():
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x, y) in danger_tiles:
                pygame.draw.rect(screen, RED, rect)
            else:
                pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # grid lines

def draw_dog():
    rect = pygame.Rect(dog_pos[0]*TILE_SIZE, dog_pos[1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.ellipse(screen, BLUE, rect)

def draw_ui():
    text = font.render(f"Lives: {lives}   Stage: {stage}", True, BLACK)
    screen.blit(text, (10, WINDOW_SIZE + 10))

# --- INIT ---
danger_tiles = generate_danger_tiles(stage)

# --- MAIN LOOP ---
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and dog_pos[1] > 0:
        dog_pos[1] -= 1
    elif keys[pygame.K_DOWN] and dog_pos[1] < GRID_SIZE - 1:
        dog_pos[1] += 1
    elif keys[pygame.K_LEFT] and dog_pos[0] > 0:
        dog_pos[0] -= 1
    elif keys[pygame.K_RIGHT] and dog_pos[0] < GRID_SIZE - 1:
        dog_pos[0] += 1

    # --- Game logic ---
    if tuple(dog_pos) in danger_tiles:
        lives -= 1
        print("Hit danger tile! Lives:", lives)
        dog_pos = [0, 0]  # reset position
        if lives <= 0:
            print("Game Over! Stray couldn't survive...")
            running = False
    
    # Reached goal (bottom-right)
    if dog_pos == [GRID_SIZE-1, GRID_SIZE-1]:
        stage += 1
        if stage > 3:  # only 3 stages
            print("You helped the stray reach safety!")
            running = False
        else:
            dog_pos = [0, 0]
            danger_tiles = generate_danger_tiles(stage)
            print(f"Stage {stage} begins!")

    # --- Draw ---
    screen.fill(WHITE)
    draw_grid()
    draw_dog()
    draw_ui()
    pygame.display.flip()
