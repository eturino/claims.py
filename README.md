# Claims

Port of [`claims.ts`](https://github.com/eturino/claims.ts)

## Usage

### Ability:

-   `ability = build_ability(permitted=["read:*", "admin:something"], prohibited=["admin:bad"])`
-   `ability.can("read:stuff")`: `bool`
-   `ability.cannot("admin:others")`: `bool`
-   `ability.is_explicitly_prohibited("admin:bad.inside")`: `bool`
-   `ability.access_to_resources("read:clients")` returns a `KeySet`

### ClaimSet

-   `claim_set = build_claim_set(["read:*", "admin:something"])`
-   `claim_set.check("read:stuff")`: `bool`
-   `claim_set.direct_children_of("read:stuff")`: `List[str]`
-   `claim_set.direct_descendants_of("read:stuff")`: `List[str]`
-   `claim_set.add_if_not_checked("read:stuff")`: `ClaimSet` (same instance if `claim_set.check("read:stuff")` is True, a new one with the claim added otherwise).

### Claim

-   `claim = build_claim("read:*")`
-   `claim.is_global()`: `bool`
-   `claim.has_verb("read")`: `bool`
-   `claim.has_resource("*")`: `bool`
-   `claim.is_exact("read:*")`: `bool`
-   `claim.check("read:stuff")`: `bool`
-   `claim.direct_child_of("read:stuff")`: `Optional[str]`
-   `claim.direct_descendant_of("read:stuff")`: `Optional[str]`
-   `claim.is_direct_child_of("read:stuff")`: `bool`
-   `claim.is_direct_descendant_of("read:stuff")`: `bool`

### Valid verbs

"admin", "read", "delete", "create", "update", "manage"
