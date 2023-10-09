"""Claim object."""
from typing import Annotated, Any, List, Optional, Union

from pydantic import BaseModel, Field

from claims.parsing import QueryTuple, RawQuery, extract_verb_resource


class Claim(BaseModel):
    """Models a single claim: `verb:resource` or `verb:*`."""

    verb: Annotated[str, Field(frozen=True)]
    resource: Annotated[Optional[str], Field(frozen=True)]

    model_config = {"frozen": True}

    def __lt__(self, other: Any) -> bool:
        """Compares based first on verb, then on resource (not Claims first)."""
        return self.__cmp__(other) < 0

    def __le__(self, other: Any) -> bool:
        """Compares based first on verb, then on resource (not Claims first)."""
        return self.__cmp__(other) <= 0

    def __gt__(self, other: Any) -> bool:
        """Compares based first on verb, then on resource (not Claims first)."""
        return self.__cmp__(other) > 0

    def __ge__(self, other: Any) -> bool:
        """Compares based first on verb, then on resource (not Claims first)."""
        return self.__cmp__(other) >= 0

    def __cmp__(self, other: Any) -> int:
        """Compares based first on verb, then on resource (not Claims first)."""
        if not isinstance(other, Claim):
            return -1
        verb_cmp = _compare_strings(a=self.verb, b=other.verb)
        if verb_cmp != 0:
            return verb_cmp
        return _compare_strings(a=self.resource, b=other.resource)

    def __str__(self) -> str:
        """Returns `VERB:*` if global or `VERB:RESOURCE otherwise."""
        suffix = "*" if self.resource is None else self.resource
        return f"{self.verb}:{suffix}"

    def __unicode__(self) -> str:
        """Returns `VERB:*` if global or `VERB:RESOURCE otherwise."""
        return self.__str__()

    def is_global(self) -> bool:
        """True if this claims represents every resource of a verb (global)."""
        return self.resource is None

    def has_verb(self, verb: str) -> bool:
        """True if this claim has the given verb."""
        return self.verb == verb

    def has_resource(self, resource: Optional[str]) -> bool:
        """
        True if this claim has the given resource.

        If the given resource is None or "*", returns true if the claim is global
        """
        if resource is None or resource == "*":
            return self.resource is None
        return self.resource == resource

    def is_exact(self, query: RawQuery) -> bool:
        """True if this claims represents exactly the same as the given query."""
        verb, resource = extract_verb_resource(query)
        return self.has_verb(verb) and self.has_resource(resource)

    def check(self, query: RawQuery) -> bool:
        """Returns true if this claim includes the given query."""
        verb, resource = extract_verb_resource(query)
        if not self.has_verb(verb):
            return False

        if self.is_global():
            return True

        if resource is None:
            return False

        if self.has_resource(resource):
            return True

        return resource.startswith(f"{self.resource}.")

    def direct_child_of(self, query: RawQuery) -> Optional[str]:
        """
        Given a query, if this claim is a direct child of that query,
        it will return the immediate child part, otherwise it returns None.

        e.g.
        claim = build_claim("read:what.some.stuff");
        claim.direct_child("admin:*")  # => None
        claim.direct_child("read:*")  # => None
        claim.direct_child("read:what")  # => None
        claim.direct_child("read:what.some")  # => "stuff"
        claim.direct_child("read:what.some.stuff")  # => None
        claim.direct_child("read:what.some.stuff.blah")  # => None
        """
        verb, resource = extract_verb_resource(query)
        if self.resource is None or not self.has_verb(verb):
            return None

        my_parts = _extract_parts(self.resource)
        resource_parts = _extract_parts(resource)
        if len(my_parts) != (len(resource_parts) + 1):
            return None

        if resource is None:
            return my_parts[0]

        if not self.resource.startswith(f"{resource}."):
            return None

        return f"{self.resource}".replace(f"{resource}.", "")

    def is_direct_child_of(self, query: RawQuery) -> bool:
        """
        Given a query, if this claim is a direct child of that query,
        it will return True.

        e.g.
        claim = build_claim("read:what.some.stuff");
        claim.direct_child("admin:*")  # => False
        claim.direct_child("read:*")  # => False
        claim.direct_child("read:what")  # => False
        claim.direct_child("read:what.some")  # => True
        claim.direct_child("read:what.some.stuff")  # => False
        claim.direct_child("read:what.some.stuff.blah")  # => False
        """
        return self.direct_child_of(query) is not None

    def direct_descendant_of(self, query: RawQuery) -> Optional[str]:
        """
        Given a query, if this claim is a direct descendant of that query,
        it will return the immediate child part, otherwise it returns None.

        e.g.
        claim = build_claim("read:what.some.stuff");
        claim.direct_descendant("admin:*")  # => None
        claim.direct_descendant("read:*")  # => "what"
        claim.direct_descendant("read:what")  # => "some"
        claim.direct_descendant("read:what.some")  # => "stuff"
        claim.direct_descendant("read:what.some.stuff")  # => None
        claim.direct_descendant("read:what.some.stuff.blah")  # => None
        """
        verb, resource = extract_verb_resource(query)
        if self.resource is None or not self.has_verb(verb):
            return None

        my_parts = _extract_parts(self.resource)

        if resource is None:
            return my_parts[0]

        if not self.resource.startswith(f"{resource}."):
            return None

        resource_parts = _extract_parts(resource)
        idx = len(resource_parts)
        return my_parts[idx]

    def is_direct_descendant_of(self, query: RawQuery) -> bool:
        """
        Given a query, if this claim is a direct descendant of that query,
        it will return True.

        e.g.
        claim = build_claim("read:what.some.stuff");
        claim.direct_descendant("admin:*")  # => False
        claim.direct_descendant("read:*")  # => True
        claim.direct_descendant("read:what")  # => True
        claim.direct_descendant("read:what.some")  # => True
        claim.direct_descendant("read:what.some.stuff")  # => False
        claim.direct_descendant("read:what.some.stuff.blah")  # => False
        """
        return self.direct_descendant_of(query) is not None


def build_claim(raw: Union[Claim, str, QueryTuple]) -> Claim:
    """Parses the raw string and builds a claim with it."""
    if isinstance(raw, Claim):
        return raw

    verb, resource = extract_verb_resource(raw)
    return Claim(verb=verb, resource=resource)


def _extract_parts(resource: Optional[str]) -> List[str]:
    if resource is None:
        return []
    return resource.split(".")


def _compare_strings(a: Optional[str], b: Optional[str]) -> int:
    a_s = "" if a is None else a
    b_s = "" if b is None else b
    if a_s == b_s:
        return 0
    if a_s < b_s:
        return -1
    return 1
