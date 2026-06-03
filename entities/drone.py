import math
import random
import pygame
from collections import deque

from core.settings import MAP_COLS, MAP_ROWS
from core.colors import GREEN, GREEN_SOFT, BLUE, RED, ORANGE, WHITE, BG
from utils.helpers import lerp, grid_to_screen, draw_text
from utils.effects import glow_circle


class Drone:
    """Gerencia movimentação, estados, ataque e renderização de drones."""

    def __init__(self, did, x, y, audio_system, log_system):
        """Inicializa um drone.
        
        Args:
            did: ID único do drone
            x: Coordenada X inicial no grid
            y: Coordenada Y inicial no grid
            audio_system: Instância do AudioSystem
            log_system: Instância do LogSystem
        """
        self.id = did

        self.x = float(x)
        self.y = float(y)

        self.render_x = float(x)
        self.render_y = float(y)

        self.base = (x, y)

        self.speed = 2.1

        self.target = None

        self.state = "PATRULHANDO"

        self.attack_timer = 0

        self.trail = deque(maxlen=45)

        self.patrol_target = self.random_patrol()

        self.audio_system = audio_system
        self.log_system = log_system

    def random_patrol(self):
        """Gera um ponto de patrulha aleatório.
        
        Returns:
            Tupla (x, y) com o novo ponto de patrulha
        """
        return (
            random.randint(1, 14),
            random.randint(1, 9),
        )

    def move_to(self, tx, ty, dt):
        """Move o drone em direção a um ponto alvo.
        
        Args:
            tx: Coordenada X do alvo
            ty: Coordenada Y do alvo
            dt: Delta time em segundos
            
        Returns:
            Distância até o alvo
        """
        dx = tx - self.x
        dy = ty - self.y

        dist = math.hypot(dx, dy)

        if dist > 0.01:
            self.x += (dx / dist) * self.speed * dt
            self.y += (dy / dist) * self.speed * dt

        return dist

    def update(self, dt, game):
        """Atualiza o drone.
        
        Args:
            dt: Delta time em segundos
            game: Referência ao objeto Game para adicionar explosões
        """
        if self.state == "PATRULHANDO":
            px, py = self.patrol_target

            dist = self.move_to(px, py, dt)

            if dist < 0.2:
                self.patrol_target = self.random_patrol()

        elif self.state == "DESIGNADO":
            pass

        elif self.state == "ATRIBUÍDO":
            if self.target and self.target.alive:
                orbit_angle = pygame.time.get_ticks() * 0.002

                offset_x = math.cos(orbit_angle) * 0.8
                offset_y = math.sin(orbit_angle) * 0.8

                dist = self.move_to(
                    self.target.x + offset_x,
                    self.target.y + offset_y,
                    dt,
                )

                if dist < 1.2:
                    self.state = "ATACANDO"
                    self.attack_timer = 1.4
                    self.audio_system._safe_play(self.audio_system.laser_sound)
                    self.log_system.add(f"D{self.id} travou alvo T{self.target.id}")

        elif self.state == "ATACANDO":
            self.attack_timer -= dt

            if self.attack_timer <= 0:
                if self.target:
                    from entities.explosion import Explosion
                    game.explosions.append(
                        Explosion(self.target.x, self.target.y)
                    )

                    self.audio_system._safe_play(self.audio_system.explosion_sound)

                    self.target.alive = False

                    self.log_system.add(f"T{self.target.id} eliminado")

                    self.target.selected = False

                self.target = None

                self.state = "RETORNANDO"

        elif self.state == "RETORNANDO":
            bx, by = self.base

            dist = self.move_to(bx, by, dt)

            if dist < 0.2:
                self.state = "PATRULHANDO"

                self.patrol_target = self.random_patrol()

                self.audio_system._safe_play(self.audio_system.return_sound)

                self.log_system.add(f"D{self.id} retornou")

        self.render_x = lerp(self.render_x, self.x, 0.12)
        self.render_y = lerp(self.render_y, self.y, 0.12)

        self.trail.append((self.render_x, self.render_y))

    def draw(self, screen, font_small):
        """Desenha o drone na tela.
        
        Args:
            screen: Superfície do pygame para desenho
            font_small: Fonte pequena para texto
        """
        sx, sy = grid_to_screen(self.render_x, self.render_y)

        # Trail
        if len(self.trail) > 2:
            pts = [grid_to_screen(px, py) for px, py in self.trail]

            for i in range(len(pts) - 1):
                alpha = int(255 * (i / len(pts)))

                col = (
                    0,
                    max(40, alpha // 2),
                    80,
                )

                pygame.draw.line(
                    screen,
                    col,
                    pts[i],
                    pts[i + 1],
                    2,
                )

        # Laser
        if self.state == "ATACANDO" and self.target:
            tx, ty = grid_to_screen(
                self.target.render_x,
                self.target.render_y,
            )

            pulse = abs(
                math.sin(pygame.time.get_ticks() * 0.02)
            )

            thickness = int(2 + pulse * 3)

            pygame.draw.line(
                screen,
                RED,
                (sx, sy),
                (tx, ty),
                thickness,
            )

        # Linha de designação
        if self.target and self.target.alive:
            tx, ty = grid_to_screen(
                self.target.render_x,
                self.target.render_y,
            )

            pygame.draw.line(
                screen,
                BLUE,
                (sx, sy),
                (tx, ty),
                1,
            )

        glow_circle(screen, (sx, sy), 16, GREEN, 100)

        pygame.draw.circle(screen, GREEN, (sx, sy), 8)

        pygame.draw.circle(screen, BG, (sx, sy), 4)

        pygame.draw.line(
            screen,
            GREEN_SOFT,
            (sx - 12, sy),
            (sx + 12, sy),
            1,
        )

        pygame.draw.line(
            screen,
            GREEN_SOFT,
            (sx, sy - 12),
            (sx, sy + 12),
            1,
        )

        draw_text(screen, f"D{self.id}", font_small, GREEN, sx - 12, sy + 18)
