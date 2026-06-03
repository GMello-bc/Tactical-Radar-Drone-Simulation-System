import pygame
import os


class AudioSystem:
    """Gerencia todos os sons do jogo."""

    def __init__(self):
        """Inicializa os sons do jogo."""
        # Tentar carregar sons, com fallback se não existirem
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sounds_path = os.path.join(base_path, "sounds")
        
        try:
            self.select_sound = pygame.mixer.Sound(
                os.path.join(sounds_path, "select.mp3")
            )
        except:
            self.select_sound = None

        try:
            self.launch_sound = pygame.mixer.Sound(
                os.path.join(sounds_path, "launch.mp3")
            )
        except:
            self.launch_sound = None

        try:
            self.laser_sound = pygame.mixer.Sound(
                os.path.join(sounds_path, "laser.mp3")
            )
        except:
            self.laser_sound = None

        try:
            self.explosion_sound = pygame.mixer.Sound(
                os.path.join(sounds_path, "explosion.mp3")
            )
        except:
            self.explosion_sound = None

        try:
            self.return_sound = pygame.mixer.Sound(
                os.path.join(sounds_path, "return.mp3")
            )
        except:
            self.return_sound = None

        # Configurar volumes
        if self.select_sound:
            self.select_sound.set_volume(0.4)
        if self.launch_sound:
            self.launch_sound.set_volume(0.3)
        if self.laser_sound:
            self.laser_sound.set_volume(0.2)
        if self.explosion_sound:
            self.explosion_sound.set_volume(0.4)
        if self.return_sound:
            self.return_sound.set_volume(0.1)

    def _safe_play(self, sound):
        """Toca um som com segurança."""
        if sound:
            try:
                sound.play()
            except:
                pass
