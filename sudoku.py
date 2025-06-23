import pygame
import sys

pygame.init()

# Constants
GRID_SIZE = 9
CELL_SIZE = 60
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
LIGHT_BLUE = (173, 216, 230)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)

class SudokuGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 40))
        pygame.display.set_caption("Sudoku Game")
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        self.small_font = pygame.font.Font(None, 24)
        self.selected_cell = None
        self.game_won = False
        self.difficulty = 0
        self.difficulty_names = ["Super Easy", "Easy", "Medium", "Hard"]
        self.grids = [
            # Super Easy
            [[5, 3, 4, 6, 7, 8, 9, 1, 2],
             [6, 7, 2, 1, 9, 5, 3, 4, 8],
             [1, 9, 8, 3, 4, 2, 5, 6, 7],
             [8, 5, 9, 7, 6, 1, 4, 2, 3],
             [4, 2, 6, 8, 5, 3, 7, 9, 1],
             [7, 1, 3, 9, 2, 4, 8, 5, 6],
             [9, 6, 1, 5, 3, 7, 2, 8, 4],
             [2, 8, 7, 4, 1, 9, 6, 3, 5],
             [3, 4, 5, 2, 8, 6, 1, 7, 0]],
            # Easy
            [[5, 3, 0, 0, 7, 0, 0, 0, 0],
             [6, 0, 0, 1, 9, 5, 0, 0, 0],
             [0, 9, 8, 0, 0, 0, 0, 6, 0],
             [8, 0, 0, 0, 6, 0, 0, 0, 3],
             [4, 0, 0, 8, 0, 3, 0, 0, 1],
             [7, 0, 0, 0, 2, 0, 0, 0, 6],
             [0, 6, 0, 0, 0, 0, 2, 8, 0],
             [0, 0, 0, 4, 1, 9, 0, 0, 5],
             [0, 0, 0, 0, 8, 0, 0, 7, 9]],
            # Medium
            [[0, 0, 0, 6, 0, 0, 4, 0, 0],
             [7, 0, 0, 0, 0, 3, 6, 0, 0],
             [0, 0, 0, 0, 9, 1, 0, 8, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 5, 0, 1, 8, 0, 0, 0, 3],
             [0, 0, 0, 3, 0, 6, 0, 4, 5],
             [0, 4, 0, 2, 0, 0, 0, 6, 0],
             [9, 0, 3, 0, 0, 0, 0, 0, 0],
             [0, 2, 0, 0, 0, 0, 1, 0, 0]],
            # Hard
            [[0, 0, 0, 0, 0, 0, 0, 1, 0],
             [4, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 6, 0, 2],
             [0, 0, 0, 0, 3, 0, 0, 0, 0],
             [5, 0, 8, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 4, 0, 0, 0],
             [0, 0, 0, 2, 0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0, 0, 0, 0, 3],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        ]
        self.grid = [row[:] for row in self.grids[self.difficulty]]

    def draw_grid(self):
        for i in range(GRID_SIZE + 1):
            thickness = 3 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), thickness)
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), thickness)

    def draw_numbers(self):
        selected_number = None
        if self.selected_cell:
            row, col = self.selected_cell
            selected_number = self.grid[row][col] if self.grid[row][col] != 0 else None

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] != 0:
                    # Highlight cells with same number as selected
                    if selected_number and self.grid[row][col] == selected_number:
                        pygame.draw.rect(self.screen, LIGHT_BLUE, 
                                       (col * CELL_SIZE + 1, row * CELL_SIZE + 1, 
                                        CELL_SIZE - 2, CELL_SIZE - 2))
                    
                    text = self.font.render(str(self.grid[row][col]), True, BLACK)
                    text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2,
                                                    row * CELL_SIZE + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)

    def draw_selection(self):
        if self.selected_cell:
            row, col = self.selected_cell
            pygame.draw.rect(self.screen, BLUE, 
                           (col * CELL_SIZE + 1, row * CELL_SIZE + 1, 
                            CELL_SIZE - 2, CELL_SIZE - 2), 3)

    def handle_click(self, pos):
        x, y = pos
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
            self.selected_cell = (row, col)

    def is_valid_sudoku(self):
        # Check if grid is complete and valid
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.grid[row][col] == 0:
                    return False
        return True

    def handle_key(self, key):
        if key == pygame.K_SPACE:
            self.difficulty = (self.difficulty + 1) % 4
            self.grid = [row[:] for row in self.grids[self.difficulty]]
            self.game_won = False
        elif self.selected_cell and pygame.K_1 <= key <= pygame.K_9:
            row, col = self.selected_cell
            self.grid[row][col] = key - pygame.K_0
            if self.is_valid_sudoku():
                self.game_won = True

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)

            self.screen.fill(WHITE)
            self.draw_numbers()
            self.draw_selection()
            self.draw_grid()
            
            # Draw difficulty level
            diff_text = self.small_font.render(f"Difficulty: {self.difficulty_names[self.difficulty]} (Press SPACE to change)", True, GREEN)
            self.screen.blit(diff_text, (10, WINDOW_SIZE + 10))
            
            if self.game_won:
                text = self.big_font.render("SUCCESS!", True, (0, 255, 0))
                text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
                pygame.draw.rect(self.screen, WHITE, text_rect.inflate(20, 20))
                self.screen.blit(text, text_rect)
            
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SudokuGame()
    game.run()
