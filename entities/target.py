import math
import random
import pygame

from core.settings import MAP_COLS, MAP_ROWS, BASE_X, BASE_Y
from core.colors import RED, BLUE
from utils.helpers import lerp, grid_to_screen, draw_text
from utils.effects import glow_circle


class Target:
    """IA do alvo com movimentação e renderização."""

    def __init__(self, tid, x, y):
        """Inicializa um alvo.
        
        Args:
            tid: ID único do alvo
            x: Coordenada X inicial no grid
            y: Coordenada Y inicial no grid
        """
        self.id = tid

        self.x = float(x)
        self.y = float(y)

        self.render_x = float(x)
        self.render_y = float(y)

        self.alive = True

        self.speed = 0.45

        self.pulse = random.random() * 10

        self.goal = self.random_goal()

        self.move_timer = random.uniform(1.5, 3.5)

        self.selected = False

    def random_goal(self):
        """Gera um objetivo aleatório evitando a base.
        
        Returns:
            Tupla (x, y) com o novo objetivo
        """
        while True:
            gx = random.randint(1, MAP_COLS - 2)
            gy = random.randint(1, MAP_ROWS - 2)

            dist = math.hypot(gx - BASE_X, gy - BASE_Y)

            if dist > 4:
                return gx, gy

    def update(self, dt):
        """Atualiza o alvo.
        
        Args:
            dt: Delta time em segundos
        """
        if not self.alive:
            return

        self.pulse += dt * 3

        self.move_timer -= dt

        if self.move_timer <= 0:
            self.goal = self.random_goal()
            self.move_timer = random.uniform(2, 4)

        gx, gy = self.goal

        dx = gx - self.x
        dy = gy - self.y

        dist = math.hypot(dx, dy)

        if dist > 0.05:
            self.x += (dx / dist) * self.speed * dt
            self.y += (dy / dist) * self.speed * dt

        # Repelir da base
        base_dist = math.hypot(self.x - BASE_X, self.y - BASE_Y)

        if base_dist < 3.8:
            angle = math.atan2(self.y - BASE_Y, self.x - BASE_X)

            self.x += math.cos(angle) * dt * 2
            self.y += math.sin(angle) * dt * 2

        self.render_x = lerp(self.render_x, self.x, 0.08)
        self.render_y = lerp(self.render_y, self.y, 0.08)

    def draw(self, screen, font_small):
        """Desenha o alvo na tela.
        
        Args:
            screen: Superfície do pygame para desenho
            font_small: Fonte pequena para texto
        """
        if not self.alive:
            return

        sx, sy = grid_to_screen(self.render_x, self.render_y)

        size = 10 + math.sin(self.pulse) * 2

        glow_circle(screen, (sx, sy), 20, RED, 80)

        points = [
            (sx, sy - size),
            (sx + size, sy),
            (sx, sy + size),
            (sx - size, sy),
        ]

        pygame.draw.polygon(screen, RED, points, 2)

        if self.selected:
            pygame.draw.circle(screen, BLUE, (sx, sy), 24, 2)

        draw_text(screen, f"T{self.id}", font_small, RED, sx - 10, sy + 18)
