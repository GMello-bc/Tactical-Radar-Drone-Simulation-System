import pygame
import math

from core.colors import GREEN, RED, WHITE
from utils.helpers import draw_text
from utils.effects import glow_circle


class Button:
    """Representa um botão genérico na tela."""

    def __init__(self, rect, label, color, font_small):
        """Inicializa um botão.
        
        Args:
            rect: pygame.Rect com posição e tamanho
            label: Texto do botão
            color: Cor RGB do botão
            font_small: Fonte para o texto
        """
        self.rect = rect
        self.label = label
        self.color = color
        self.font = font_small
        self.hovered = False

    def check_hover(self, mouse_pos):
        """Verifica se o mouse está sobre o botão.
        
        Args:
            mouse_pos: Tupla (x, y) da posição do mouse
            
        Returns:
            True se o mouse está sobre o botão
        """
        self.hovered = self.rect.collidepoint(mouse_pos)
        return self.hovered

    def draw(self, screen, bg_color=(10, 20, 20)):
        """Desenha o botão na tela.
        
        Args:
            screen: Superfície do pygame para desenho
            bg_color: Cor de fundo do botão
        """
        if self.hovered:
            glow = pygame.Surface(
                (self.rect.w + 20, self.rect.h + 20),
                pygame.SRCALPHA,
            )

            pygame.draw.rect(
                glow,
                (*self.color, 40),
                (0, 0, self.rect.w + 20, self.rect.h + 20),
                border_radius=12,
            )

            screen.blit(glow, (self.rect.x - 10, self.rect.y - 10))

        pygame.draw.rect(screen, bg_color, self.rect, border_radius=10)

        pygame.draw.rect(
            screen,
            self.color,
            self.rect,
            2,
            border_radius=10,
        )

        draw_text(
            screen,
            self.label,
            self.font,
            self.color,
            self.rect.x + 72 if len(self.label) > 4 else self.rect.x + 34,
            self.rect.y + 15 if self.rect.h > 40 else self.rect.y + 9,
        )
