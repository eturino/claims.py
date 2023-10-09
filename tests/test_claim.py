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
from claims.claim import Claim, build_claim
from claims.errors import InvalidClaimError, InvalidClaimVerbError


class TestClaim:  # noqa: D101
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
            build_claim(raw)

    @pytest.mark.parametrize("raw", ["blah:what", "blah:*"])
    def test_build_error_invalid_verb(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimVerbError):
            build_claim(raw)

    @pytest.mark.parametrize(
        "valid_verb", ["admin", "read", "delete", "create", "update", "manage"]
    )
    def test_valid_verbs(self, valid_verb: str) -> None:  # noqa: D102, D103
        cleaned = f"{valid_verb}:what"
        actual_list = [
            build_claim(f"{valid_verb}:what"),
            build_claim(f"{valid_verb}:what.*"),
        ]
        for actual in actual_list:
            assert isinstance(actual, Claim)
            assert str(actual) == cleaned
            assert actual.__str__() == cleaned
            assert actual.__unicode__() == cleaned
            assert actual.verb == valid_verb
            assert actual.resource == "what"
            assert actual.has_verb(valid_verb)
            assert not actual.has_verb("other")
            assert actual.has_resource("what")
            assert not actual.has_resource("other")
            assert not actual.has_resource("*")
            assert not actual.has_resource(None)
            assert not actual.is_global()

    def test_admin_global(self) -> None:  # noqa: D102, D103
        actual = build_claim("admin:*")
        assert isinstance(actual, Claim)
        assert str(actual) == "admin:*"
        assert actual.__str__() == "admin:*"
        assert actual.__unicode__() == "admin:*"
        assert actual.verb == "admin"
        assert actual.resource is None
        assert actual.has_verb("admin")
        assert not actual.has_verb("other")
        assert actual.has_resource("*")
        assert actual.has_resource(None)
        assert not actual.has_resource("what")
        assert not actual.has_resource("other")
        assert actual.is_global()

    def test_equality(self) -> None:  # noqa: D102, D103
        c1 = build_claim("admin:*")
        c2 = build_claim("admin:*")
        assert c1 == c2

    def test_lt(self) -> None:  # noqa: D102, D103
        c1 = build_claim("admin:*")
        c2 = build_claim("admin:something")
        assert c1 < c2

    @pytest.mark.parametrize(
        "query", ["", "oiasjdoaiejfa.aoeifjao", "read:stuffOIAJFEA!#!#!"]
    )
    def test_check_error_invalid_query(self, query: str) -> None:  # noqa: D102, D103
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimError):
            claim.check(query)

    @pytest.mark.parametrize("query", ["blah:what", "blah:what.*", "blah:*"])
    def test_check_error_invalid_verb(self, query: str) -> None:  # noqa: D102, D103
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimVerbError):
            claim.check(query)

    def test_claim_read_global_check(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:*")
        assert claim.check("read:*")
        assert claim.check("read:something.else")
        assert not claim.check("admin:*")

    def test_claim_read_check(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:something")
        assert not claim.check("read:*")
        assert claim.check("read:something")
        assert claim.check("read:something.else")
        assert not claim.check("admin:*")
        assert not claim.check("admin:something")

    @pytest.mark.parametrize(
        "query", ["", "oiasjdoaiejfa.aoeifjao", "read:stuffOIAJFEA!#!#!"]
    )
    def test_exact_error_invalid_query(self, query: str) -> None:  # noqa: D102, D103
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimError):
            claim.is_exact(query)

    @pytest.mark.parametrize("query", ["blah:what", "blah:what.*", "blah:*"])
    def test_exact_error_invalid_verb(self, query: str) -> None:  # noqa: D102, D103
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimVerbError):
            claim.is_exact(query)

    def test_claim_read_global_is_exact(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:*")
        assert claim.is_exact("read:*")
        assert not claim.is_exact("read:something.else")
        assert not claim.is_exact("admin:*")

    def test_claim_read_is_exact(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:something")
        assert not claim.is_exact("read:*")
        assert claim.is_exact("read:something")
        assert not claim.is_exact("read:something.else")
        assert not claim.is_exact("admin:*")
        assert not claim.is_exact("admin:something")

    def test_claim_read_global_direct_child_of(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:*")
        _assert_not_child(claim, "read:*")
        _assert_not_child(claim, "read:something")
        _assert_not_child(claim, "read:something.else")
        _assert_not_child(claim, "read:something.else.deep")
        _assert_not_child(claim, "admin:*")
        _assert_not_child(claim, "admin:something")
        _assert_not_child(claim, "admin:something.else")

    def test_claim_read_direct_child_of(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:something")
        _assert_child(claim, "read:*", "something")
        _assert_not_child(claim, "read:something")
        _assert_not_child(claim, "read:something.else")
        _assert_not_child(claim, "read:something.else.deep")
        _assert_not_child(claim, "admin:*")
        _assert_not_child(claim, "admin:something")
        _assert_not_child(claim, "admin:something.else")

    def test_claim_read_nested_direct_child_of(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:something.else")
        _assert_not_child(claim, "read:*")
        _assert_child(claim, "read:something", "else")
        _assert_not_child(claim, "read:something.else")
        _assert_not_child(claim, "read:something.else.deep")
        _assert_not_child(claim, "admin:*")
        _assert_not_child(claim, "admin:something")
        _assert_not_child(claim, "admin:something.else")

    def test_claim_read_global_direct_descendant_of(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:*")
        _assert_not_descendant(claim, "read:*")
        _assert_not_descendant(claim, "read:something")
        _assert_not_descendant(claim, "read:something.else")
        _assert_not_descendant(claim, "read:something.else.deep")
        _assert_not_descendant(claim, "admin:*")
        _assert_not_descendant(claim, "admin:something")
        _assert_not_descendant(claim, "admin:something.else")

    def test_claim_read_direct_descendant_of(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:something")
        _assert_descendant(claim, "read:*", "something")
        _assert_not_descendant(claim, "read:something")
        _assert_not_descendant(claim, "read:something.else")
        _assert_not_descendant(claim, "read:something.else.deep")
        _assert_not_descendant(claim, "admin:*")
        _assert_not_descendant(claim, "admin:something")
        _assert_not_descendant(claim, "admin:something.else")

    def test_claim_read_nested_direct_descendant_of(self) -> None:  # noqa: D102, D103
        claim = build_claim("read:something.else")
        _assert_descendant(claim, "read:*", "something")
        _assert_descendant(claim, "read:something", "else")
        _assert_not_descendant(claim, "read:something.else")
        _assert_not_descendant(claim, "read:something.else.deep")
        _assert_not_descendant(claim, "admin:*")
        _assert_not_descendant(claim, "admin:something")
        _assert_not_descendant(claim, "admin:something.else")

    @pytest.mark.parametrize(
        "query", ["", "oiasjdoaiejfa.aoeifjao", "read:stuffOIAJFEA!#!#!"]
    )
    def test_direct_child_error_invalid_query(  # noqa: D102, D103
        self, query: str
    ) -> None:
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimError):
            claim.direct_child_of(query)

    @pytest.mark.parametrize("query", ["blah:what", "blah:what.*", "blah:*"])
    def test_direct_child_error_invalid_verb(  # noqa: D102, D103
        self, query: str
    ) -> None:
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimVerbError):
            claim.direct_child_of(query)

    @pytest.mark.parametrize(
        "query", ["", "oiasjdoaiejfa.aoeifjao", "read:stuffOIAJFEA!#!#!"]
    )
    def test_is_direct_child_of_error_invalid_query(  # noqa: D102, D103
        self, query: str
    ) -> None:
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimError):
            claim.is_direct_child_of(query)

    @pytest.mark.parametrize("query", ["blah:what", "blah:what.*", "blah:*"])
    def test_is_direct_child_of_error_invalid_verb(  # noqa: D102, D103
        self, query: str
    ) -> None:
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimVerbError):
            claim.is_direct_child_of(query)

    @pytest.mark.parametrize(
        "query", ["", "oiasjdoaiejfa.aoeifjao", "read:stuffOIAJFEA!#!#!"]
    )
    def test_direct_descendant_error_invalid_query(  # noqa: D102, D103
        self, query: str
    ) -> None:
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimError):
            claim.direct_descendant_of(query)

    @pytest.mark.parametrize("query", ["blah:what", "blah:what.*", "blah:*"])
    def test_direct_descendant_error_invalid_verb(  # noqa: D102, D103
        self, query: str
    ) -> None:
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimVerbError):
            claim.direct_descendant_of(query)

    @pytest.mark.parametrize(
        "query", ["", "oiasjdoaiejfa.aoeifjao", "read:stuffOIAJFEA!#!#!"]
    )
    def test_is_direct_descendant_of_error_invalid_query(  # noqa: D102, D103
        self, query: str
    ) -> None:
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimError):
            claim.is_direct_descendant_of(query)

    @pytest.mark.parametrize("query", ["blah:what", "blah:what.*", "blah:*"])
    def test_is_direct_descendant_of_error_invalid_verb(  # noqa: D102, D103
        self, query: str
    ) -> None:
        claim = build_claim("read:*")

        with pytest.raises(InvalidClaimVerbError):
            claim.is_direct_descendant_of(query)


def _assert_not_child(claim: Claim, query: str) -> None:
    assert claim.direct_child_of(query) is None
    assert not claim.is_direct_child_of(query)


def _assert_child(claim: Claim, query: str, child: str) -> None:
    assert claim.direct_child_of(query) == child
    assert claim.is_direct_child_of(query)


def _assert_not_descendant(claim: Claim, query: str) -> None:
    assert claim.direct_descendant_of(query) is None
    assert not claim.is_direct_descendant_of(query)


def _assert_descendant(claim: Claim, query: str, child: str) -> None:
    assert claim.direct_descendant_of(query) == child
    assert claim.is_direct_descendant_of(query)
