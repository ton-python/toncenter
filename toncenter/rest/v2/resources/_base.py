from __future__ import annotations

import typing as t

from pydantic import ValidationError

from toncenter.client import _get_adapter
from toncenter.exceptions import ToncenterValidationError, raise_for_status

if t.TYPE_CHECKING:
    from toncenter.rest.client import ToncenterRestClient

__all__ = [
    "BaseResource",
]

_T = t.TypeVar("_T")


class BaseResource:
    """Base class for all API resource groups."""

    _PATH_PREFIX: t.ClassVar[str] = "/api/v2"

    def __init__(self, client: ToncenterRestClient) -> None:
        self._client = client

    @t.overload
    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: type[_T],
    ) -> _T: ...

    @t.overload
    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: None = None,
    ) -> t.Any: ...

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, t.Any] | None = None,
        body: t.Any | None = None,
        headers: dict[str, t.Any] | None = None,
        response_model: type[_T] | None = None,
    ) -> _T | t.Any:
        """Delegate an HTTP request to the underlying client.

        The v2 API wraps every response in ``{"ok": true, "result": ...}``.
        This method extracts the ``result`` value and optionally validates
        it against *response_model* using ``pydantic.TypeAdapter``
        (supports regular models, union aliases, and generic types like
        ``list[Model]``).

        When the v2 API returns HTTP 200 with ``"ok": false`` in the body
        (e.g. liteserver errors), the embedded ``code`` is used to raise
        the appropriate ``ToncenterStatusError``.

        :param method: HTTP method.
        :param path: API path.
        :param params: Query parameters.
        :param body: JSON request body.
        :param headers: Additional request headers.
        :param response_model: Type to validate the ``result`` against.
        :return: Parsed model instance or raw value.
        """
        data = await self._client.request(
            method,
            f"{self._PATH_PREFIX}{path}",
            params=params,
            body=body,
            headers=headers,
        )
        if isinstance(data, dict) and data.get("ok") is False:
            error = data.get("error", "Unknown error")
            code = data.get("code", 500)
            raise_for_status(code, str(error))
        result = data.get("result") if isinstance(data, dict) else data
        if response_model is not None:
            try:
                return _get_adapter(response_model).validate_python(result)
            except ValidationError as exc:
                raise ToncenterValidationError(
                    model=response_model,
                    errors=exc.errors(),
                ) from exc
        return result
