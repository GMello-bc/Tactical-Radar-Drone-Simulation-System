import math
import random
import pygame

from core.colors import ORANGE, RED, YELLOW
from utils.helpers import grid_to_screen


class Explosion:
    """Gerencia explosões e partículas."""

    def __init__(self, x, y):
        """Inicializa uma explosão.
        
        Args:
            x: Coordenada X no grid
            y: Coordenada Y no grid
        """
        self.x = x
        self.y = y

        self.life = 1.0
        self.radius = 0

        self.particles = []

        for _ in range(50):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1, 6)

            self.particles.append(
                {
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": random.uniform(0.3, 1.0),
                }
            )

    def update(self, dt):
        """Atualiza a explosão.
        
        Args:
            dt: Delta time em segundos
        """
        self.life -= dt

        self.radius += 240 * dt

        for p in self.particles:
            p["x"] += p["vx"] * dt * 60
            p["y"] += p["vy"] * dt * 60

            p["life"] -= dt

    def draw(self, screen):
        """Desenha a explosão na tela.
        
        Args:
            screen: Superfície do pygame para desenho
        """
        sx, sy = grid_to_screen(self.x, self.y)

        if self.life > 0:
            pygame.draw.circle(
                screen,
                ORANGE,
                (sx, sy),
                int(self.radius),
                2,
            )

            pygame.draw.circle(
                screen,
                RED,
                (sx, sy),
                int(self.radius * 0.6),
                2,
            )

        for p in self.particles:
            if p["life"] <= 0:
                continue

            px, py = grid_to_screen(p["x"], p["y"])

            pygame.draw.circle(
                screen,
                YELLOW,
                (px, py),
                2,
            )
