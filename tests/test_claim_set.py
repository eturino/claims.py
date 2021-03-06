# -*- coding: utf-8 -*-

"""Basic test suite.

There are some 'noqa: F401' in this file to just test the isort import sorting
along with the code formatter.
"""

import __future__  # noqa: F401

import json  # noqa: F401
from os import path  # noqa: F401
from re import IGNORECASE, sub  # noqa: F401

import pytest

import claims  # noqa: F401
from claims.claim import build_claim
from claims.claim_set import ClaimSet, build_claim_set
from claims.errors import InvalidClaimError, InvalidClaimVerbError


class TestClaimSet:  # noqa: D101
    @pytest.mark.parametrize(
        "raw",
        [
            "",  # empty string
            "whatever.stuff",  # no verb
            "read:stuffOIAJFEA!#!#!",  # bad chars
        ],
    )
    def test_build_errors_bad_raw(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimError):
            build_claim_set(["read:valid", raw])

    @pytest.mark.parametrize("raw", ["blah:what", "blah:*"])
    def test_build_errors_bad_verb(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimVerbError):
            build_claim_set(["read:valid", raw])

    @pytest.mark.parametrize(
        "raw",
        [
            "",  # empty string
            "whatever.stuff",  # no verb
            "read:stuffOIAJFEA!#!#!",  # bad chars
        ],
    )
    def test_check_errors_bad_raw(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimError):
            cs = build_claim_set(["read:valid"])
            cs.check(raw)

    @pytest.mark.parametrize("raw", ["blah:what", "blah:*"])
    def test_check_errors_bad_verb(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimVerbError):
            cs = build_claim_set(["read:valid"])
            cs.check(raw)

    def test_build_uniq_sort(self) -> None:  # noqa: D102, D103
        actual = build_claim_set(["admin:*", "read:valid", "admin:*"])
        claim_admin = build_claim("admin:*")
        claim_read = build_claim("read:valid")
        expected_claims = [claim_admin, claim_read]
        assert isinstance(actual, ClaimSet)
        assert len(actual.claims) == len(expected_claims)
        for idx, a in enumerate(actual.claims):
            b = expected_claims[idx]
            assert a == b

    def test_check_valid(self) -> None:  # noqa: D102, D103
        actual = build_claim_set(["admin:*", "read:valid", "admin:*"])
        assert actual.check("admin:something")

    def test_check_invalid(self) -> None:  # noqa: D102, D103
        actual = build_claim_set(["admin:*", "read:valid", "admin:*"])
        assert not actual.check("read:something")

    @pytest.mark.parametrize(
        "raw",
        [
            "",  # empty string
            "whatever.stuff",  # no verb
            "read:stuffOIAJFEA!#!#!",  # bad chars
        ],
    )
    def test_direct_children_errors_bad_raw(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimError):
            cs = build_claim_set(["read:valid"])
            cs.direct_children_of(raw)

    @pytest.mark.parametrize("raw", ["blah:what", "blah:*"])
    def test_direct_children_errors_bad_verb(  # noqa: D102, D103
        self, raw: str
    ) -> None:
        with pytest.raises(InvalidClaimVerbError):
            cs = build_claim_set(["read:valid"])
            cs.direct_children_of(raw)

    def test_direct_children_of_valid(self) -> None:  # noqa: D102, D103
        c1 = build_claim("read:*")
        c2 = build_claim("admin:valid")
        c3 = build_claim("admin:valid.other")
        c4 = build_claim("admin:valid.another")
        c5 = build_claim("admin:wow")
        actual = build_claim_set([c1, c2, c3, c4, c5])

        assert actual.direct_children_of("admin:valid") == ["another", "other"]

    def test_direct_descendants_of_valid(self) -> None:  # noqa: D102, D103
        c1 = build_claim("read:*")
        c2 = build_claim("admin:valid")
        c3 = build_claim("admin:valid.other")
        c4 = build_claim("admin:valid.another")
        c5 = build_claim("admin:amber")
        actual = build_claim_set([c1, c2, c3, c4, c5])

        assert actual.direct_descendants_of("admin:*") == ["amber", "valid"]
