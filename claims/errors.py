"""Exception classes that can be raised when building claims."""


class InvalidClaimError(Exception):
    """The given string doesn't have the correct format to be parsed as claim."""

    def __init__(self, raw_string: str):
        """
        The given string doesn't have the correct format to be parsed as claim.

        Stores the raw_string and sets the message
        """
        self.raw_string = raw_string
        self.message = f"The given string cannot be parsed as claim: {raw_string}"
        super().__init__(self.message)


class InvalidClaimVerbError(Exception):
    """The given string doesn't have the right verb."""

    def __init__(self, verb: str):
        """
        The given string doesn't have the right verb.

        Stores the verb and sets the message
        """
        self.verb = verb
        self.message = f"The given verb cannot be parsed as claim's valid verb: {verb}"
        super().__init__(self.message)
