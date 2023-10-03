"""Ability object."""

from typing import Sequence, Union

import key_set
from pydantic import BaseModel, Field

from claims.claim import Claim
from claims.claim_set import ClaimSet, build_claim_set
from claims.parsing import QueryTuple, RawQuery, extract_verb_resource


class Ability(BaseModel):
    """Models an ability with permitted and prohibited claims"""

    permitted: ClaimSet = Field(frozen=True)
    prohibited: ClaimSet = Field(frozen=True)

    model_config = {"frozen": True}

    def can(self, query: RawQuery) -> bool:
        """Returns true if a permitted claim checks, and no prohibited claim check."""
        query_tuple = extract_verb_resource(query)
        return self.permitted.check(query_tuple) and not self.prohibited.check(
            query_tuple
        )

    def cannot(self, query: RawQuery) -> bool:
        """Inverse of can."""
        return not self.can(query)

    def is_explicitly_prohibited(self, query: RawQuery) -> bool:
        """Returns true if a prohibited claim checks, regardless of permitted."""
        return self.prohibited.check(query)

    def access_to_resources(self, query: RawQuery) -> key_set.KeySet:
        """
        Returns a KeySet describing the access of this ability to the
        children of the given query:
        Allows on direct descendants, forbids on direct children
        """
        qt = extract_verb_resource(query)
        allowed = (
            key_set.build_all()
            if self.permitted.check(qt)
            else key_set.build_some_or_none(self.permitted.direct_descendants_of(qt))
        )
        forbidden = (
            key_set.build_all()
            if self.prohibited.check(qt)
            else key_set.build_some_or_none(self.prohibited.direct_children_of(qt))
        )
        return allowed.difference(forbidden)


def build_ability(
    permitted: Sequence[Union[Claim, str, QueryTuple]],
    prohibited: Sequence[Union[Claim, str, QueryTuple]],
) -> Ability:
    """Builds an Ability from the 2 lists of raw claims: permitted and prohibited."""
    permitted_claim_set = build_claim_set(permitted)
    prohibited_claim_set = build_claim_set(prohibited)
    return Ability(permitted=permitted_claim_set, prohibited=prohibited_claim_set)
