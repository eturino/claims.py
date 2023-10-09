"""ClaimSet object, which represents a list of claims."""
from typing import Any, Callable, List, Optional, Sequence, Set, Union

from pydantic import BaseModel, Field, model_validator

from claims.claim import Claim, build_claim
from claims.parsing import QueryTuple, RawQuery, extract_verb_resource


class ClaimSet(BaseModel):
    """Models a list of claims"""

    claims: List[Claim] = Field(default_factory=list, frozen=True)

    model_config = {"frozen": True}

    @model_validator(mode="before")
    @classmethod
    def parse_claims(cls, data: Any) -> Any:
        """Parses the claims from the data, if it is a dict."""
        if isinstance(data, dict):
            assert "claims" in data, "claims should be included"
            data["claims"] = build_claim_list(data["claims"])
        return data

    def check(self, query: RawQuery) -> bool:
        """Returns True if any of the claims checks for the given query."""
        query_tuple = extract_verb_resource(query)
        for claim in self.claims:
            if claim.check(query_tuple):
                return True
        return False

    def add_if_not_checked(self, query: RawQuery) -> "ClaimSet":
        """If the query is checked, returns self. Otherwise, it returns a new Claim with this query added."""
        if self.check(query):
            return self

        claims = self.claims.copy()
        claims.append(build_claim(query))
        sorted_claims = sorted(claims)
        return ClaimSet(claims=sorted_claims)

    def direct_children_of(self, query: RawQuery) -> List[str]:
        """
        Collects from the claims of the set the result of `direct_child_of()`.
        Removes Nones
        """
        return self._map_in_claims(
            query, child_for=lambda claim, qt: claim.direct_child_of(qt)
        )

    def direct_descendants_of(self, query: RawQuery) -> List[str]:
        """
        Collects from the claims of the set the result of `direct_descendant_of()`.
        Removes Nones
        """
        return self._map_in_claims(
            query, child_for=lambda claim, qt: claim.direct_descendant_of(qt)
        )

    def _map_in_claims(
        self, query: RawQuery, child_for: Callable[[Claim, QueryTuple], Optional[str]]
    ) -> List[str]:
        query_tuple = extract_verb_resource(query)
        children_set: Set[str] = set()
        for claim in self.claims:
            child = child_for(claim, query_tuple)
            if child is not None:
                children_set.add(child)

        return sorted(list(children_set))


def build_claim_set(
    raw_list: ClaimSet | Sequence[Union[Claim, str, QueryTuple]]
) -> ClaimSet:
    """Given a list of raw claims and returns a ClaimSet with the parsed claims."""
    if isinstance(raw_list, ClaimSet):
        return raw_list

    return ClaimSet(claims=build_claim_list(raw_list))


def build_claim_list(raw_list: Sequence[Union[Claim, str, QueryTuple]]) -> List[Claim]:
    """Given a list of raw claims and returns a list of parsed claims."""
    raw_set = set(raw_list)
    claims = [build_claim(x) for x in raw_set]

    return sorted(claims)
