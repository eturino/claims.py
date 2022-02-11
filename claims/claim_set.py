"""ClaimSet object, which represents a list of claims."""
from typing import Callable, List, Optional, Set, Union

from attr import define, field

from claims.claim import Claim, build_claim
from claims.parsing import QueryTuple, RawQuery, extract_verb_resource


@define(frozen=True, eq=True, repr=True, init=True)
class ClaimSet:
    """Models a list of claims"""

    claims: List[Claim] = field()

    def check(self, query: RawQuery) -> bool:
        """Returns True if any of the claims checks for the given query."""
        query_tuple = extract_verb_resource(query)
        for claim in self.claims:
            if claim.check(query_tuple):
                return True
        return False

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


def build_claim_set(raw_list: List[Union[Claim, str, QueryTuple]]) -> ClaimSet:
    """Given a list of raw claims and returns a ClaimSet with the parsed claims."""
    raw_set = set(raw_list)
    claims = [build_claim(x) for x in raw_set]

    return ClaimSet(claims=sorted(claims))
