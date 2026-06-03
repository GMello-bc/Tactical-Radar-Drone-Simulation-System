from collections import deque


class LogSystem:
    """Gerencia os eventos do sistema."""

    def __init__(self):
        """Inicializa o sistema de logs."""
        self.logs = deque(maxlen=7)

    def add(self, text):
        """Adiciona um novo log."""
        self.logs.appendleft(text)
