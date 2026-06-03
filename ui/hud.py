import math
import pygame

from core.colors import GRID, GREEN, BG
from core.settings import MAP_X, MAP_Y, MAP_COLS, MAP_ROWS, CELL, BASE_X, BASE_Y, WIDTH
from utils.helpers import draw_text, grid_to_screen
from utils.effects import glow_circle


class HUD:
    """Elementos da interface gráfica: título, grid, base e radar."""

    def __init__(self, font_big, font_med):
        """Inicializa o HUD.
        
        Args:
            font_big: Fonte grande para título
            font_med: Fonte média para subtítulo
        """
        self.font_big = font_big
        self.font_med = font_med
        self.sweep = 0

    def update(self, dt):
        """Atualiza o HUD.
        
        Args:
            dt: Delta time em segundos
        """
        self.sweep += dt * 60

    def draw_title(self, screen):
        """Desenha o título e subtítulo.
        
        Args:
            screen: Superfície do pygame para desenho
        """
        draw_text(screen, "RADAR TÁTICO", self.font_big, GREEN, 42, 24)

        draw_text(
            screen,
            "SISTEMA DE COMANDO DE DRONES",
            self.font_med,
            (130, 190, 170),
            44,
            66,
        )

    def draw_grid(self, screen):
        """Desenha o grid do mapa.
        
        Args:
            screen: Superfície do pygame para desenho
        """
        for x in range(MAP_COLS + 1):
            px = MAP_X + x * CELL

            pygame.draw.line(
                screen,
                GRID,
                (px, MAP_Y),
                (px, MAP_Y + MAP_ROWS * CELL),
                1,
            )

        for y in range(MAP_ROWS + 1):
            py = MAP_Y + y * CELL

            pygame.draw.line(
                screen,
                GRID,
                (MAP_X, py),
                (MAP_X + MAP_COLS * CELL, py),
                1,
            )

    def draw_base(self, screen):
        """Desenha a base e o radar de varredura.
        
        Args:
            screen: Superfície do pygame para desenho
        """
        bx, by = grid_to_screen(BASE_X, BASE_Y)

        for r in range(40, 170, 30):
            pygame.draw.circle(
                screen,
                (0, 70, 45),
                (bx, by),
                r,
                1,
            )

        sweep_surface = pygame.Surface((420, 420), pygame.SRCALPHA)

        ex = 210 + math.cos(math.radians(self.sweep)) * 190
        ey = 210 + math.sin(math.radians(self.sweep)) * 190

        pygame.draw.polygon(
            sweep_surface,
            (0, 255, 140, 30),
            [
                (210, 210),
                (ex, ey),
                (ex - 20, ey - 20),
            ],
        )

        screen.blit(sweep_surface, (bx - 210, by - 210))

        glow_circle(screen, (bx, by), 20, GREEN, 100)

        pygame.draw.circle(screen, GREEN, (bx, by), 10)

        draw_text(screen, "BASE", self.font_med, GREEN, bx - 28, by + 24)

    def draw(self, screen):
        """Desenha todos os elementos do HUD.
        
        Args:
            screen: Superfície do pygame para desenho
        """
        self.draw_title(screen)
        self.draw_grid(screen)
        self.draw_base(screen)
