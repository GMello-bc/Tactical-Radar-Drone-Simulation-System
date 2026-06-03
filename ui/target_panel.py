import pygame

from core.colors import PANEL, GREEN, RED, BLUE
from utils.helpers import draw_text
from utils.effects import glow_circle


class TargetPanel:
    """Painel de alvos disponíveis para designação."""

    def __init__(self, x, y, width, height, font_med, font_small):
        """Inicializa o painel de alvos.
        
        Args:
            x: Posição X
            y: Posição Y
            width: Largura do painel
            height: Altura do painel
            font_med: Fonte média para título
            font_small: Fonte pequena para dados
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_med = font_med
        self.font_small = font_small
        self.button_data = []

    def update_buttons(self, targets):
        """Atualiza os botões dos alvos.
        
        Args:
            targets: Lista de alvos
        """
        self.button_data.clear()

        visible_targets = [t for t in targets if t.alive]

        for i, target in enumerate(visible_targets):
            bx = self.x
            by = self.y + i * 64

            rect = pygame.Rect(bx, by, self.width, 44)
            self.button_data.append((rect, target))

    def draw(self, screen, mouse_pos):
        """Desenha o painel de alvos.
        
        Args:
            screen: Superfície do pygame para desenho
            mouse_pos: Posição do mouse
        """
        draw_text(
            screen,
            "ALVOS DISPONÍVEIS",
            self.font_med,
            GREEN,
            self.x,
            self.y - 50,
        )

        for rect, target in self.button_data:
            hovered = rect.collidepoint(mouse_pos)

            bg_col = (15, 10, 12)
            border_col = RED

            if target.selected:
                bg_col = (20, 25, 40)
                border_col = BLUE

            if hovered:
                glow = pygame.Surface(
                    (rect.w + 20, rect.h + 20),
                    pygame.SRCALPHA,
                )

                pygame.draw.rect(
                    glow,
                    (*border_col, 40),
                    (0, 0, rect.w + 20, rect.h + 20),
                    border_radius=12,
                )

                screen.blit(glow, (rect.x - 10, rect.y - 10))

            pygame.draw.rect(screen, bg_col, rect, border_radius=10)

            pygame.draw.rect(
                screen,
                border_col,
                rect,
                2,
                border_radius=10,
            )

            draw_text(
                screen,
                f"ALVO T{target.id}",
                self.font_small,
                border_col,
                rect.x + 20,
                rect.y + 12,
            )

    def get_clicked_target(self, mouse_pos):
        """Retorna o alvo clicado ou None.
        
        Args:
            mouse_pos: Posição do mouse
            
        Returns:
            Target ou None
        """
        for rect, target in self.button_data:
            if rect.collidepoint(mouse_pos):
                return target
        return None
