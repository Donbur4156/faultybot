"""
decorator.py

This module defines utility functions for creating slash command options.
"""

from interactions import OptionType, slash_option


def teamname_option():
    """
    A decorator for adding a "teamname" option to a function.

    This option is typically used in Discord slash commands.

    Usage:
        @teamname_option()
        async def my_command(ctx, teamname):
            # Your command logic here
    """

    def wrapper(func):
        return slash_option(
            name="teamname",
            description="Teamname to check",
            opt_type=OptionType.STRING,
            required=True,
        )(func)

    return wrapper
