from interactions import OptionType, slash_option


def teamname_option():
    def wrapper(func):
        return slash_option(
            name="teamname",
            description="teamname to check",
            opt_type=OptionType.STRING,
            required=True,
        )(func)

    return wrapper
