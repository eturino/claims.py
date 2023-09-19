# -*- coding: utf-8 -*-
"""Utility functions."""
import re
from typing import Optional, Tuple, Union

from claims.errors import InvalidClaimError, InvalidClaimVerbError

QueryTuple = Tuple[str, Optional[str]]
RawQuery = Union[str, QueryTuple]


# allows for the optional `.*` at the end, (ignored on Claim creation)
CLAIM_REGEX = re.compile(r"^([\w_\-]+):([\w_.\-]+\w)(\.\*)?$")

# cater for `read: *` global claims
GLOBAL_WILDCARD_CLAIM_REGEX = re.compile(r"^([\w_\-]+):\*$")


def extract_verb_resource(raw: RawQuery) -> QueryTuple:
    """Returns a tuple with (verb, resource) from the raw string."""
    if isinstance(raw, tuple):
        return raw

    global_match = GLOBAL_WILDCARD_CLAIM_REGEX.match(raw)
    if global_match:
        return _check_and_build(global_match.group(1), None)

    claim_match = CLAIM_REGEX.match(raw)
    if claim_match:
        return _check_and_build(claim_match.group(1), claim_match.group(2))

    raise InvalidClaimError(raw)


def _check_and_build(verb: str, resource: Optional[str]) -> QueryTuple:
    if verb not in ALLOWED_VERBS:
        raise InvalidClaimVerbError(verb)

    return verb, resource


ALLOWED_VERBS = ["admin", "read", "delete", "create", "update", "manage"]
