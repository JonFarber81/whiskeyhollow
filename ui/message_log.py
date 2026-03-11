"""In-game message log with period-appropriate flavor."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Reversible, Tuple

import tcod.console

from ui import color as Color
from constants import MAX_MESSAGES


@dataclass
class Message:
    plain_text: str
    fg: Tuple[int, int, int] = field(default_factory=lambda: Color.MSG_DEFAULT)

    @property
    def full_text(self) -> str:
        return self.plain_text


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
        self,
        text: str,
        fg: Tuple[int, int, int] = Color.MSG_DEFAULT,
    ) -> None:
        self.messages.append(Message(text, fg))
        if len(self.messages) > MAX_MESSAGES:
            self.messages.pop(0)

    def render(
        self,
        console: tcod.console.Console,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> None:
        """Render the last N messages that fit in the given area."""
        self._render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def _render_messages(
        console: tcod.console.Console,
        x: int,
        y: int,
        width: int,
        height: int,
        messages: Reversible[Message],
    ) -> None:
        y_offset = height - 1
        for message in reversed(messages):
            # Word-wrap each message
            lines = MessageLog._wrap(message.plain_text, width - 2)
            for line in reversed(lines):
                if y_offset < 0:
                    return
                console.print(x=x + 1, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1

    @staticmethod
    def _wrap(text: str, width: int) -> List[str]:
        """Simple word-wrap."""
        words = text.split()
        lines: List[str] = []
        current = ""
        for word in words:
            if current:
                test = current + " " + word
            else:
                test = word
            if len(test) <= width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines if lines else [""]
