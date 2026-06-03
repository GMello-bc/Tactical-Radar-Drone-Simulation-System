import pygame


def glow_circle(surface, pos, radius, color, alpha=100):
    """Desenha um círculo com efeito de brilho."""
    glow = pygame.Surface(
        (radius * 4, radius * 4),
        pygame.SRCALPHA
    )

    for r in range(radius * 2, 0, -4):
        a = int(alpha * (r / (radius * 2)))

        pygame.draw.circle(
            glow,
            (*color, a),
            (radius * 2, radius * 2),
            r,
        )

    surface.blit(
        glow,
        (
            pos[0] - radius * 2,
            pos[1] - radius * 2,
        ),
    )
