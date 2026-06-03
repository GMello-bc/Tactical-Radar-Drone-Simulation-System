import pygame
from core.settings import MAP_X, MAP_Y, CELL


def lerp(a, b, t):
    """Interpolação linear entre dois valores."""
    return a + (b - a) * t


def draw_text(screen, text, font, color, x, y):
    """Renderiza texto na tela."""
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))


def grid_to_screen(x, y):
    """Converte coordenadas do grid para coordenadas de tela."""
    sx = MAP_X + x * CELL + CELL // 2
    sy = MAP_Y + y * CELL + CELL // 2
    return sx, sy