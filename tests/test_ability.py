# -*- coding: utf-8 -*-

"""Basic test suite.

There are some 'noqa: F401' in this file to just test the isort import sorting
along with the code formatter.
"""

import __future__  # noqa: F401

import json  # noqa: F401
from os import path  # noqa: F401
from re import IGNORECASE, sub  # noqa: F401
from typing import List

import key_set
import pytest

import claims  # noqa: F401
from claims import Claim, build_claim
from claims.ability import build_ability
from claims.errors import InvalidClaimError, InvalidClaimVerbError


class TestAbility:  # noqa: D101
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
            build_ability(["read:valid", raw], [])

    @pytest.mark.parametrize("raw", ["blah:what", "blah:*"])
    def test_build_errors_bad_verb(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimVerbError):
            build_ability(["read:valid", raw], [])

    @pytest.mark.parametrize(
        "raw",
        [
            "",  # empty string
            "whatever.stuff",  # no verb
            "read:stuffOIAJFEA!#!#!",  # bad chars
        ],
    )
    def test_can_errors_bad_raw(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimError):
            actual = build_ability(["read:valid"], [])
            actual.can(raw)

    @pytest.mark.parametrize("raw", ["blah:what", "blah:*"])
    def test_can_errors_bad_verb(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimVerbError):
            actual = build_ability(["read:valid"], [])
            actual.can(raw)

    @pytest.mark.parametrize(
        "raw",
        [
            "",  # empty string
            "whatever.stuff",  # no verb
            "read:stuffOIAJFEA!#!#!",  # bad chars
        ],
    )
    def test_cannot_errors_bad_raw(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimError):
            actual = build_ability(["read:valid"], [])
            actual.cannot(raw)

    @pytest.mark.parametrize("raw", ["blah:what", "blah:*"])
    def test_cannot_errors_bad_verb(self, raw: str) -> None:  # noqa: D102, D103
        with pytest.raises(InvalidClaimVerbError):
            actual = build_ability(["read:valid"], [])
            actual.cannot(raw)

    @pytest.mark.parametrize(
        "raw",
        [
            "",  # empty string
            "whatever.stuff",  # no verb
            "read:stuffOIAJFEA!#!#!",  # bad chars
        ],
    )
    def test_is_explicitly_prohibited_errors_bad_raw(  # noqa: D102, D103
        self, raw: str
    ) -> None:
        with pytest.raises(InvalidClaimError):
            actual = build_ability(["read:valid"], [])
            actual.is_explicitly_prohibited(raw)

    @pytest.mark.parametrize("raw", ["blah:what", "blah:*"])
    def test_is_explicitly_prohibited_errors_bad_verb(  # noqa: D102, D103
        self, raw: str
    ) -> None:
        with pytest.raises(InvalidClaimVerbError):
            actual = build_ability(["read:valid"], [])
            actual.is_explicitly_prohibited(raw)

    def test_can_true(self) -> None:  # noqa: D102, D103
        actual = build_ability(["read:valid"], [])
        assert actual.can("read:valid.some.stuff")

    def test_can_prohibited(self) -> None:  # noqa: D102, D103
        actual = build_ability(["read:valid"], ["read:valid.not"])
        assert not actual.can("read:valid.not.stuff")

    def test_can_not_present(self) -> None:  # noqa: D102, D103
        actual = build_ability(["read:valid"], [])
        assert not actual.can("read:another")

    def test_cannot_true(self) -> None:  # noqa: D102, D103
        actual = build_ability(["read:valid"], [])
        assert not actual.cannot("read:valid.some.stuff")

    def test_cannot_prohibited(self) -> None:  # noqa: D102, D103
        actual = build_ability(["read:valid"], ["read:valid.not"])
        assert actual.cannot("read:valid.not.stuff")

    def test_cannot_not_present(self) -> None:  # noqa: D102, D103
        actual = build_ability(["read:valid"], [])
        assert actual.cannot("read:another")

    def test_explicitly_prohibited_true(self) -> None:  # noqa: D102, D103
        actual = build_ability(["read:valid"], [])
        assert not actual.is_explicitly_prohibited("read:valid.some.stuff")

    def test_explicitly_prohibited_prohibited(self) -> None:  # noqa: D102, D103
        actual = build_ability(["read:valid"], ["read:valid.not"])
        assert actual.is_explicitly_prohibited("read:valid.not.stuff")

    def test_explicitly_prohibited_not_present(self) -> None:  # noqa: D102, D103
        actual = build_ability(["read:valid"], [])
        assert not actual.is_explicitly_prohibited("read:another")

    def test_access_to_resources_direct(self) -> None:  # noqa: D102, D103
        ability = build_ability(["read:clients"], [])
        actual = ability.access_to_resources("read:clients")
        assert isinstance(actual, key_set.KeySetAll)

    def test_access_to_resources_negated(self) -> None:  # noqa: D102, D103
        ability = build_ability(["read:clients"], ["read:clients"])
        actual = ability.access_to_resources("read:clients")
        assert isinstance(actual, key_set.KeySetNone)

    def test_access_to_resources_aes(self) -> None:  # noqa: D102, D103
        ability = build_ability(["read:clients"], ["read:clients.a"])
        actual = ability.access_to_resources("read:clients")
        assert isinstance(actual, key_set.KeySetAllExceptSome)
        assert actual.elements() == {"a"}

    def test_access_to_resources_some_1(self) -> None:  # noqa: D102, D103
        ability = build_ability(["read:clients.a", "read:clients.b"], [])
        actual = ability.access_to_resources("read:clients")
        assert isinstance(actual, key_set.KeySetSome)
        assert actual.elements() == {"a", "b"}

    def test_access_to_resources_some_2(self) -> None:  # noqa: D102, D103
        ability = build_ability(
            ["read:clients.a.nested", "read:clients.b.nested", "read:clients.c"],
            ["read:clients.b"],
        )
        actual = ability.access_to_resources("read:clients")
        assert isinstance(actual, key_set.KeySetSome)
        assert actual.elements() == {"a", "c"}

    def test_access_to_resources_none_surviving(self) -> None:  # noqa: D102, D103
        ability = build_ability(
            ["read:clients.a.nested", "read:clients.b.nested", "read:clients.c"],
            ["read:clients"],
        )
        actual = ability.access_to_resources("read:clients")
        assert isinstance(actual, key_set.KeySetNone)

    def test_access_to_resources_negating_nested(self) -> None:  # noqa: D102, D103
        ability = build_ability(
            ["read:clients.a", "read:clients.b"], ["read:clients.a.people"]
        )
        actual = ability.access_to_resources("read:clients")
        assert isinstance(actual, key_set.KeySetSome)
        assert actual.elements() == {"a", "b"}

    def test_access_to_resources_deep_all(self) -> None:  # noqa: D102, D103
        ability = build_ability(["read:clients"], [])
        actual = ability.access_to_resources("read:clients.my-client.projects.project")
        assert isinstance(actual, key_set.KeySetAll)

    def test_access_to_resources_deep_none(self) -> None:  # noqa: D102, D103
        permitted: List[Claim] = [build_claim("read:clients")]
        prohibited: List[Claim] = [
            build_claim("read:clients.my-client.projects.project")
        ]
        ability = build_ability(permitted, prohibited)
        actual = ability.access_to_resources("read:clients.my-client.projects.project")
        assert isinstance(actual, key_set.KeySetNone)

    def test_access_to_resources_deep_none_2(self) -> None:  # noqa: D102, D103
        ability = build_ability(["read:clients.another"], [])
        actual = ability.access_to_resources("read:clients.my-client.projects.project")
        assert isinstance(actual, key_set.KeySetNone)

    def test_access_to_resources_deep_aes(self) -> None:  # noqa: D102, D103
        ability = build_ability(
            ["read:clients"],
            ["read:clients.my-client.projects.project.bad-project"],
        )
        actual = ability.access_to_resources("read:clients.my-client.projects.project")
        assert isinstance(actual, key_set.KeySetAllExceptSome)
        assert actual.elements() == {"bad-project"}

    def test_access_to_resources_deep_some_but_people(self) -> None:  # noqa: D102, D103
        ability = build_ability(
            [
                "read:clients.my-client.projects.project.one-project",
                "read:clients.my-client.projects.project.bad-project",
            ],
            [
                "read:clients.my-client.projects.project.one-project.people",
                "read:clients.my-client.projects.project.bad-project",
            ],
        )
        actual = ability.access_to_resources("read:clients.my-client.projects.project")
        assert isinstance(actual, key_set.KeySetSome)
        assert actual.elements() == {"one-project"}
