import random
from PIL import Image, ImageDraw

COLS = 53
ROWS = 7
CELL_SIZE = 10
CELL_PADDING = 2
FRAMES = 30  
BG_COLOR = (13, 17, 23) 

COLORS = [
    (22, 27, 34),   
    (14, 68, 41),   
    (0, 109, 50),   
    (38, 166, 65),  
    (57, 211, 83)   
]

def init_grid():
    return [[random.choice([0, 1]) for _ in range(COLS)] for _ in range(ROWS)]

def get_neighbors(grid, r, c):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue
            nr, nc = r + i, c + j
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                count += grid[nr][nc]
    return count

def evolve(grid):
    new_grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    for r in range(ROWS):
        for c in range(COLS):
            neighbors = get_neighbors(grid, r, c)
            if grid[r][c] == 1:
                if neighbors in [2, 3]:
                    new_grid[r][c] = 1
            else:
                if neighbors == 3:
                    new_grid[r][c] = 1
    return new_grid

def draw_frame(grid):
    width = COLS * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
    height = ROWS * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    for r in range(ROWS):
        for c in range(COLS):
            x = c * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
            y = r * (CELL_SIZE + CELL_PADDING) + CELL_PADDING
            
            color_idx = 4 if grid[r][c] == 1 else 0
            
            draw.rectangle(
                [x, y, x + CELL_SIZE, y + CELL_SIZE],
                fill=COLORS[color_idx],
                outline=None,
                width=0
            )

    return img

def main():
    grid = init_grid()
    images = []
    
    for _ in range(FRAMES):
        img = draw_frame(grid)
        images.append(img)
        grid = evolve(grid)
        
        if sum(sum(row) for row in grid) == 0:
            grid = init_grid()

    images[0].save(
        "github-contribution-grid-snake.gif",
        save_all=True,
        append_images=images[1:],
        duration=200,
        loop=0
    )

if __name__ == "__main__":
    main()