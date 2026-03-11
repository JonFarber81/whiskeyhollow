"""Custom exceptions for Whiskey Hollow."""


class QuitGame(Exception):
    """Raised to signal the game should exit cleanly."""


class Impossible(Exception):
    """Raised when an action cannot be performed (e.g. blocked path, no item)."""


class PlayerDead(Exception):
    """Raised when the player is killed — triggers game over screen."""


class PlayerWon(Exception):
    """Raised when a win condition is met — triggers victory screen."""
