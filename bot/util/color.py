"""
colors.py

This module defines an Enum class for colors using the Color class from discord-py-interactions.

It provides a convenient way to reference color codes in Discord interactions.

Example Usage:
    from colors import Colors

    def set_embed_color(embed, color):
        embed.color = color.value

    # Set embed color to RED
    set_embed_color(my_embed, Colors.RED)

Attributes:
    RED (int): Red color code.
    ORANGE (int): Orange color code.
    TBGBLAU (int): Turquoise/Blue color code.
    GREEN (int): Green color code.
    VIOLET (int): Violet color code.
    BLACK (int): Black color code.
    YELLOW (int): Yellow color code.
    BLUE (int): Blue color code.
"""

from enum import Enum
from interactions import Color  # pkg: pip install discord-py-interactions


class Colors(Color, Enum):
    """
    Enumerated colors using the Color class from discord-py-interactions.

    Attributes:
        RED (int): Red color code.
        ORANGE (int): Orange color code.
        TBGBLAU (int): Turquoise/Blue color code.
        GREEN (int): Green color code.
        VIOLET (int): Violet color code.
        BLACK (int): Black color code.
        YELLOW (int): Yellow color code.
        BLUE (int): Blue color code.
    """

    RED = 0xCE3636
    ORANGE = 0xF48942
    TBGBLAU = 0x0D5EAF
    GREEN = 0x36CE36
    VIOLET = 0x9B59B6
    BLACK = 0x2F3136
    YELLOW = 0xFFA800
    BLUE = 0x0000FF
