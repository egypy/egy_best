class BotDetectedException(Exception):
    """raised when the ip is detected as a bot.

    in some cased it raised also due the geolocation restriction
    """

    def __init__(self):
        """Class constructor.

        passing a custom string to the parent class Exception
        """
        msg = 'Bot Has Been detected, Try using a proxy or change the headers'
        super().__init__(msg)


class TranslateNotFound(Exception):
    """raised when no translation found."""

    def __init__(self):
        """Class constructor.

        passing a custom string to the parent class Exception
        """
        msg = """No Translation has been found"""
        super().__init__(msg)
