import sys
import math
import pygame

# Inicializar pygame ANTES de importar settings
pygame.init()
pygame.mixer.init()

from core.settings import (
    FPS, MAP_COLS, MAP_ROWS,
    RIGHT_W, BASE_X, BASE_Y
)
import core.settings as settings
from core.colors import (
    BG, GREEN, RED, BLUE, ORANGE, TEXT, PANEL
)
from entities import Drone, Target, Explosion
from systems.audio_system import AudioSystem
from systems.log_system import LogSystem
from utils.helpers import grid_to_screen
from ui.buttons import Button
from ui.drone_panel import DronePanel
from ui.target_panel import TargetPanel
from ui.logs_panel import LogsPanel
from ui.hud import HUD


class Game:
    """Classe principal que controla o jogo inteiro."""

    def __init__(self):
        """Inicializa o jogo."""
        # Atualizar dimensões de tela dinâmicas
        info = pygame.display.Info()
        settings.WIDTH = info.current_w
        settings.HEIGHT = info.current_h
        settings.RIGHT_X = settings.WIDTH - settings.RIGHT_W - 40
        
        self.WIDTH = settings.WIDTH
        self.HEIGHT = settings.HEIGHT
        self.RIGHT_X = settings.RIGHT_X
        self.RIGHT_W = settings.RIGHT_W

        # Modo de tela
        self.fullscreen = settings.FULLSCREEN
        self.create_screen()

        pygame.display.set_caption("Radar Tático")

        self.clock = pygame.time.Clock()

        # Fontes
        self.font_small = pygame.font.SysFont("consolas", 15)
        self.font_med = pygame.font.SysFont("consolas", 20, bold=True)
        self.font_big = pygame.font.SysFont("consolas", 36, bold=True)

        # Sistemas
        self.audio_system = AudioSystem()
        self.log_system = LogSystem()

        # Entidades
        self.drones = [
            Drone(1, BASE_X, BASE_Y, self.audio_system, self.log_system),
            Drone(2, BASE_X, BASE_Y, self.audio_system, self.log_system),
            Drone(3, BASE_X, BASE_Y, self.audio_system, self.log_system),
        ]

        self.targets = [
            Target(1, 2, 1),
            Target(2, 13, 2),
            Target(3, 12, 9),
            Target(4, 1, 8),
            Target(5, 6, 2),
            Target(6, 14, 7),
        ]

        self.explosions = []

        # UI Components
        self.hud = HUD(self.font_big, self.font_med)

        self.drone_panel = DronePanel(40, 140, 260, 260, self.font_med, self.font_small)

        self.target_panel = TargetPanel(
            self.RIGHT_X + 20, 190, 320, 44,
            self.font_med, self.font_small
        )

        self.logs_panel = LogsPanel(self.RIGHT_X + 20, self.HEIGHT - 180, self.font_med, self.font_small)

        # Botões
        self.execute_button = Button(
            pygame.Rect(self.RIGHT_X + 20, 610, 320, 52),
            "EXECUTAR MISSÃO",
            GREEN,
            self.font_small
        )

        self.exit_button = Button(
            pygame.Rect(self.WIDTH - 170, 30, 120, 42),
            "SAIR",
            RED,
            self.font_med
        )

        # Estados
        self.running = True

        # Log inicial
        self.log_system.add("Sistema operacional")

        # State colors
        self.state_colors = {
            "PATRULHANDO": GREEN,
            "DESIGNADO": BLUE,
            "ATRIBUÍDO": BLUE,
            "ATACANDO": RED,
            "RETORNANDO": ORANGE,
        }

    def create_screen(self):
        """Cria ou recria a tela no modo fullscreen ou janela."""
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (self.WIDTH, self.HEIGHT),
                pygame.FULLSCREEN
            )
        else:
            self.screen = pygame.display.set_mode(
                (self.WIDTH, self.HEIGHT)
            )

    def handle_events(self, mouse):
        """Processa eventos do jogo.
        
        Args:
            mouse: Posição do mouse
        """
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Alternar entre fullscreen e janela com F11
                if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    self.create_screen()
                    pygame.display.set_caption("Radar Tático")

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = mouse

                if self.exit_button.rect.collidepoint(mx, my):
                    self.running = False

                # Check target buttons
                clicked_target = self.target_panel.get_clicked_target((mx, my))

                if clicked_target:
                    if not clicked_target.alive:
                        return

                    available = [
                        d for d in self.drones
                        if d.state == "PATRULHANDO"
                    ]

                    if not available:
                        self.log_system.add("Nenhum drone disponível")
                        return

                    for t in self.targets:
                        t.selected = False

                    clicked_target.selected = True

                    self.audio_system._safe_play(self.audio_system.select_sound)

                    nearest = min(
                        available,
                        key=lambda d: math.hypot(
                            d.x - clicked_target.x,
                            d.y - clicked_target.y,
                        ),
                    )

                    nearest.target = clicked_target

                    nearest.state = "DESIGNADO"

                    self.log_system.add(
                        f"D{nearest.id} preparado para T{clicked_target.id}"
                    )

                # Check execute button
                if self.execute_button.rect.collidepoint(mx, my):
                    for drone in self.drones:
                        if drone.state == "DESIGNADO":
                            drone.state = "ATRIBUÍDO"

                    self.audio_system._safe_play(self.audio_system.launch_sound)

                    self.log_system.add("Missão iniciada")

    def update(self, dt):
        """Atualiza o estado do jogo.
        
        Args:
            dt: Delta time em segundos
        """
        # Update HUD
        self.hud.update(dt)

        # Update entities
        for target in self.targets:
            target.update(dt)

        for drone in self.drones:
            drone.update(dt, self)

        # Update explosions
        for explosion in self.explosions[:]:
            explosion.update(dt)

            if explosion.life <= 0:
                self.explosions.remove(explosion)

        # Update panels
        self.target_panel.update_buttons(self.targets)

    def draw(self, mouse):
        """Renderiza o jogo.
        
        Args:
            mouse: Posição do mouse
        """
        # Background
        self.screen.fill(BG)

        # Scanlines
        for y in range(0, self.HEIGHT, 4):
            pygame.draw.line(
                self.screen,
                (5, 5, 5),
                (0, y),
                (self.WIDTH, y),
                1,
            )

        # HUD
        self.hud.draw(self.screen)

        # Panel background
        panel = pygame.Rect(self.RIGHT_X, 100, self.RIGHT_W, 760)

        pygame.draw.rect(self.screen, PANEL, panel, border_radius=18)

        pygame.draw.rect(
            self.screen,
            (0, 80, 60),
            panel,
            1,
            border_radius=18,
        )

        # Draw entities
        for target in self.targets:
            target.draw(self.screen, self.font_small)

        for drone in self.drones:
            drone.draw(self.screen, self.font_small)

        for explosion in self.explosions:
            explosion.draw(self.screen)

        # Draw UI
        self.drone_panel.draw(self.screen, self.drones, self.state_colors)

        # Target panel
        self.target_panel.draw(self.screen, mouse)

        # Execute button
        self.execute_button.check_hover(mouse)
        self.execute_button.draw(self.screen, (10, 20, 20))

        # Logs panel
        self.logs_panel.draw(self.screen, self.log_system.logs)

        # Exit button
        self.exit_button.check_hover(mouse)
        self.exit_button.draw(self.screen, (20, 8, 10))

        # Update display
        pygame.display.flip()

    def run(self):
        """Loop principal do jogo."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            mouse = pygame.mouse.get_pos()

            self.handle_events(mouse)
            self.update(dt)
            self.draw(mouse)

        pygame.quit()
        sys.exit()
