import pygame

from core.colors import GREEN, TEXT
from utils.helpers import draw_text


class LogsPanel:
    """Painel de eventos/logs do sistema."""

    def __init__(self, x, y, font_med, font_small):
        """Inicializa o painel de logs.
        
        Args:
            x: Posição X
            y: Posição Y
            font_med: Fonte média para título
            font_small: Fonte pequena para logs
        """
        self.x = x
        self.y = y
        self.font_med = font_med
        self.font_small = font_small

    def draw(self, screen, logs):
        """Desenha o painel de logs.
        
        Args:
            screen: Superfície do pygame para desenho
            logs: Deque com os logs
        """
        draw_text(
            screen,
            "EVENTOS",
            self.font_med,
            GREEN,
            self.x,
            self.y,
        )

        for i, log in enumerate(logs):
            draw_text(
                screen,
                log,
                self.font_small,
                TEXT,
                self.x,
                self.y + 40 + i * 22,
            )
