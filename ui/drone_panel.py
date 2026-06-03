import pygame

from core.colors import PANEL, GREEN, TEXT
from utils.helpers import draw_text
from utils.effects import glow_circle


class DronePanel:
    """Painel esquerdo mostrando status dos drones."""

    def __init__(self, x, y, width, height, font_med, font_small):
        """Inicializa o painel de drones.
        
        Args:
            x: Posição X
            y: Posição Y
            width: Largura do painel
            height: Altura do painel
            font_med: Fonte média para título
            font_small: Fonte pequena para dados
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font_med = font_med
        self.font_small = font_small

    def draw(self, screen, drones, state_colors):
        """Desenha o painel de drones.
        
        Args:
            screen: Superfície do pygame para desenho
            drones: Lista de drones
            state_colors: Dicionário com cores por estado
        """
        pygame.draw.rect(
            screen,
            PANEL,
            self.rect,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            (0, 80, 60),
            self.rect,
            1,
            border_radius=18
        )

        draw_text(
            screen,
            "DRONES",
            self.font_med,
            GREEN,
            self.rect.x + 20,
            self.rect.y + 20
        )

        for i, drone in enumerate(drones):
            y = self.rect.y + 70 + i * 58

            row = pygame.Rect(
                self.rect.x + 15,
                y,
                230,
                42
            )

            pygame.draw.rect(
                screen,
                (10, 20, 22),
                row,
                border_radius=10
            )

            col = state_colors.get(
                drone.state,
                (220, 255, 240)
            )

            glow_circle(
                screen,
                (row.x + 18, row.y + 21),
                7,
                col,
                80
            )

            pygame.draw.circle(
                screen,
                col,
                (row.x + 18, row.y + 21),
                5
            )

            draw_text(
                screen,
                f"D{drone.id}",
                self.font_med,
                (220, 255, 240),
                row.x + 35,
                row.y + 10
            )

            draw_text(
                screen,
                drone.state,
                self.font_small,
                col,
                row.x + 95,
                row.y + 13
            )
