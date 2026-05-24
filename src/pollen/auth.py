"""Authentication and shop ownership helpers for Milestone 1.2."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    user_id: str
    email: str


@dataclass(frozen=True)
class Shop:
    shop_id: str
    owner_user_id: str
    name: str


@dataclass(frozen=True)
class AuthContext:
    user: User
    shop: Shop


class ManagedAuthProvider:
    """Minimal managed-auth abstraction.

    In production this would validate provider tokens and map claims.
    For milestone-safe tests we parse deterministic bearer tokens.
    """

    def authenticate(self, authorization_header: str | None) -> User | None:
        if not authorization_header:
            return None
        prefix = "Bearer "
        if not authorization_header.startswith(prefix):
            return None

        token = authorization_header[len(prefix) :]
        # Deterministic token format for tests: user:<user_id>:<email>
        parts = token.split(":")
        if len(parts) != 3 or parts[0] != "user":
            return None

        _, user_id, email = parts
        if not user_id or not email:
            return None
        return User(user_id=user_id, email=email)


class ShopRepository:
    """In-memory shop/user mapping with auto-provisioning for first login."""

    def __init__(self) -> None:
        self._shops_by_owner: dict[str, Shop] = {}

    def get_or_create_for_user(self, user: User) -> Shop:
        existing = self._shops_by_owner.get(user.user_id)
        if existing is not None:
            return existing

        created = Shop(
            shop_id=f"shop-{user.user_id}",
            owner_user_id=user.user_id,
            name=f"{user.email.split('@')[0]}'s Shop",
        )
        self._shops_by_owner[user.user_id] = created
        return created

    def has_access(self, *, user: User, shop_id: str) -> bool:
        shop = self.get_or_create_for_user(user)
        return shop.shop_id == shop_id


class AuthService:
    def __init__(
        self,
        auth_provider: ManagedAuthProvider | None = None,
        shop_repository: ShopRepository | None = None,
    ) -> None:
        self._auth_provider = auth_provider or ManagedAuthProvider()
        self._shop_repository = shop_repository or ShopRepository()

    def resolve_context(self, authorization_header: str | None) -> AuthContext | None:
        user = self._auth_provider.authenticate(authorization_header)
        if user is None:
            return None
        shop = self._shop_repository.get_or_create_for_user(user)
        return AuthContext(user=user, shop=shop)

    def can_access_shop(self, authorization_header: str | None, shop_id: str) -> bool:
        user = self._auth_provider.authenticate(authorization_header)
        if user is None:
            return False
        return self._shop_repository.has_access(user=user, shop_id=shop_id)
