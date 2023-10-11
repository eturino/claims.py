"""Exception classes that can be raised when building claims."""
from typing import Any


class InvalidClaimError(Exception):
    """The given string doesn't have the correct format to be parsed as claim."""

    def __init__(self, raw: Any):
        """
        The given string doesn't have the correct format to be parsed as claim.

        Stores the raw_string and sets the message
        """
        self.raw = raw
        self.message = f"The given string cannot be parsed as claim: {raw}"
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


class InvalidClaimResourceError(Exception):
    """The given claim resource is not valid."""

    def __init__(self, resource: Any):
        """The given claim resource is not valid."""
        self.resource = resource
        self.message = (
            f"The given resource cannot be parsed as claim's valid resource: {resource}"
        )
        super().__init__(self.message)
