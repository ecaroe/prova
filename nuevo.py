import pygame
import random
from dataclasses import dataclass

GRID_WIDTH = 10
GRID_HEIGHT = 20
CELL_SIZE = 30
SIDE_PANEL = 220
SCREEN_WIDTH = GRID_WIDTH * CELL_SIZE + SIDE_PANEL
SCREEN_HEIGHT = GRID_HEIGHT * CELL_SIZE

MID_ROW = GRID_HEIGHT // 2

BACKGROUND = (16, 16, 20)
GRID_LINE = (40, 40, 50)
MID_LINE = (90, 90, 120)
TEXT_COLOR = (230, 230, 230)

TETROMINOES = [
    {
        "name": "I",
        "color": (0, 240, 240),
        "rotations": [
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(2, 0), (2, 1), (2, 2), (2, 3)],
        ],
    },
    {
        "name": "O",
        "color": (240, 240, 0),
        "rotations": [[(1, 1), (2, 1), (1, 2), (2, 2)]],
    },
    {
        "name": "T",
        "color": (160, 0, 240),
        "rotations": [
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
        ],
    },
    {
        "name": "S",
        "color": (0, 200, 0),
        "rotations": [
            [(1, 1), (2, 1), (0, 2), (1, 2)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
        ],
    },
    {
        "name": "Z",
        "color": (220, 0, 0),
        "rotations": [
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(2, 0), (1, 1), (2, 1), (1, 2)],
        ],
    },
    {
        "name": "J",
        "color": (0, 80, 240),
        "rotations": [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ],
    },
    {
        "name": "L",
        "color": (240, 160, 0),
        "rotations": [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ],
    },
]


@dataclass
class Piece:
    x: int
    y: int
    rotations: list
    color: tuple
    rotation_index: int = 0

    @property
    def cells(self):
        return self.rotations[self.rotation_index]

    def rotate(self):
        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)

    def rotate_back(self):
        self.rotation_index = (self.rotation_index - 1) % len(self.rotations)


def new_piece(direction):
    shape = random.choice(TETROMINOES)
    start_x = GRID_WIDTH // 2 - 2
    start_y = 0 if direction == "down" else GRID_HEIGHT - 4
    return Piece(start_x, start_y, shape["rotations"], shape["color"])


def create_grid():
    return [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def is_valid(piece, grid, direction, dx=0, dy=0):
    for cell_x, cell_y in piece.cells:
        new_x = piece.x + cell_x + dx
        new_y = piece.y + cell_y + dy
        if not (0 <= new_x < GRID_WIDTH):
            return False
        if direction == "down":
            if not (0 <= new_y < MID_ROW):
                return False
        else:
            if not (MID_ROW <= new_y < GRID_HEIGHT):
                return False
        if grid[new_y][new_x] is not None:
            return False
    return True


def lock_piece(piece, grid):
    for cell_x, cell_y in piece.cells:
        grid[piece.y + cell_y][piece.x + cell_x] = piece.color


def clear_lines_top(grid):
    top_rows = grid[:MID_ROW]
    remaining = [row for row in top_rows if any(cell is None for cell in row)]
    cleared = MID_ROW - len(remaining)
    grid[:MID_ROW] = [[None] * GRID_WIDTH for _ in range(cleared)] + remaining
    return cleared


def clear_lines_bottom(grid):
    bottom_rows = grid[MID_ROW:]
    remaining = [row for row in bottom_rows if any(cell is None for cell in row)]
    cleared = len(bottom_rows) - len(remaining)
    grid[MID_ROW:] = remaining + [[None] * GRID_WIDTH for _ in range(cleared)]
    return cleared


def draw_grid(surface, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GRID_LINE, rect, 1)
            if grid[y][x] is not None:
                pygame.draw.rect(surface, grid[y][x], rect.inflate(-2, -2))

    mid_y = MID_ROW * CELL_SIZE
    pygame.draw.line(surface, MID_LINE, (0, mid_y), (GRID_WIDTH * CELL_SIZE, mid_y), 3)


def draw_piece(surface, piece):
    for cell_x, cell_y in piece.cells:
        rect = pygame.Rect(
            (piece.x + cell_x) * CELL_SIZE,
            (piece.y + cell_y) * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE,
        )
        pygame.draw.rect(surface, piece.color, rect.inflate(-2, -2))


def draw_panel(surface, font, scores):
    panel_x = GRID_WIDTH * CELL_SIZE
    panel_rect = pygame.Rect(panel_x, 0, SIDE_PANEL, SCREEN_HEIGHT)
    pygame.draw.rect(surface, (24, 24, 32), panel_rect)

    title = font.render("Duelo Tetris", True, TEXT_COLOR)
    surface.blit(title, (panel_x + 20, 20))

    controls = [
        "Jugador arriba:",
        "A/D mover",
        "S bajar",
        "W rotar",
        "",
        "Jugador abajo:",
        "←/→ mover",
        "↑ subir",
        "↓ rotar",
    ]

    offset = 70
    for line in controls:
        text = font.render(line, True, TEXT_COLOR)
        surface.blit(text, (panel_x + 20, offset))
        offset += 26

    score_y = SCREEN_HEIGHT - 120
    top_score = font.render(f"Puntos arriba: {scores['top']}", True, TEXT_COLOR)
    bottom_score = font.render(f"Puntos abajo: {scores['bottom']}", True, TEXT_COLOR)
    surface.blit(top_score, (panel_x + 20, score_y))
    surface.blit(bottom_score, (panel_x + 20, score_y + 30))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris doble")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)

    grid = create_grid()

    top_piece = new_piece("down")
    bottom_piece = new_piece("up")

    scores = {"top": 0, "bottom": 0}

    drop_timer = 0
    drop_interval = 500

    running = True
    while running:
        dt = clock.tick(60)
        drop_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if is_valid(top_piece, grid, "down", dx=-1):
                        top_piece.x -= 1
                elif event.key == pygame.K_d:
                    if is_valid(top_piece, grid, "down", dx=1):
                        top_piece.x += 1
                elif event.key == pygame.K_s:
                    if is_valid(top_piece, grid, "down", dy=1):
                        top_piece.y += 1
                elif event.key == pygame.K_w:
                    top_piece.rotate()
                    if not is_valid(top_piece, grid, "down"):
                        top_piece.rotate_back()

                if event.key == pygame.K_LEFT:
                    if is_valid(bottom_piece, grid, "up", dx=-1):
                        bottom_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if is_valid(bottom_piece, grid, "up", dx=1):
                        bottom_piece.x += 1
                elif event.key == pygame.K_UP:
                    if is_valid(bottom_piece, grid, "up", dy=-1):
                        bottom_piece.y -= 1
                elif event.key == pygame.K_DOWN:
                    bottom_piece.rotate()
                    if not is_valid(bottom_piece, grid, "up"):
                        bottom_piece.rotate_back()

        if drop_timer >= drop_interval:
            drop_timer = 0
            if is_valid(top_piece, grid, "down", dy=1):
                top_piece.y += 1
            else:
                lock_piece(top_piece, grid)
                scores["top"] += clear_lines_top(grid) * 100
                top_piece = new_piece("down")
                if not is_valid(top_piece, grid, "down"):
                    running = False

            if is_valid(bottom_piece, grid, "up", dy=-1):
                bottom_piece.y -= 1
            else:
                lock_piece(bottom_piece, grid)
                scores["bottom"] += clear_lines_bottom(grid) * 100
                bottom_piece = new_piece("up")
                if not is_valid(bottom_piece, grid, "up"):
                    running = False

        screen.fill(BACKGROUND)
        draw_grid(screen, grid)
        draw_piece(screen, top_piece)
        draw_piece(screen, bottom_piece)
        draw_panel(screen, font, scores)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
