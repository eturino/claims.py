# -*- coding: utf-8 -*-
"""Utility functions."""
import re
from typing import Optional, Tuple, TypedDict, Union

from claims.errors import (
    InvalidClaimError,
    InvalidClaimResourceError,
    InvalidClaimVerbError,
)


class ClaimDict(TypedDict):
    """Dict representation of a claim."""

    verb: str
    resource: Optional[str]


QueryTuple = Tuple[str, Optional[str]]
RawQuery = Union[str, QueryTuple, ClaimDict]


# allows for the optional `.*` at the end, (ignored on Claim creation)
CLAIM_REGEX = re.compile(r"^([\w_\-]+):([\w_.\-]+\w)(\.\*)?$")
RESOURCE_REGEX = re.compile(r"^([\w_.\-]+\w)(\.\*)?$")

# cater for `read: *` global claims
GLOBAL_WILDCARD_CLAIM_REGEX = re.compile(r"^([\w_\-]+):\*$")


def extract_verb_resource(raw: RawQuery) -> QueryTuple:
    """Returns a tuple with (verb, resource) from the raw string."""
    if isinstance(raw, tuple):
        return _check_and_build(raw[0], raw[1])

    if isinstance(raw, dict):
        try:
            verb = raw["verb"]
            resource = raw["resource"]
        except KeyError:
            raise InvalidClaimError(raw)
        return _check_and_build(verb, resource)

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

    if not resource:
        return verb, None

    if not isinstance(resource, str):
        raise InvalidClaimResourceError(resource)

    if not RESOURCE_REGEX.match(resource):
        raise InvalidClaimResourceError(resource)

    return verb, resource


ALLOWED_VERBS = ["admin", "read", "delete", "create", "update", "manage"]
