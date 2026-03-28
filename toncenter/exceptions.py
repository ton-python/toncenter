import json
import typing as t

__all__ = [
    "STREAMING_RECOVERABLE",
    "TONCENTER_STATUS_TO_EXCEPTION",
    "ToncenterBadRequestError",
    "ToncenterClientError",
    "ToncenterConflictError",
    "ToncenterConnectionError",
    "ToncenterConnectionLostError",
    "ToncenterError",
    "ToncenterForbiddenError",
    "ToncenterGatewayTimeoutError",
    "ToncenterInternalServerError",
    "ToncenterLiteServerError",
    "ToncenterMethodNotAllowedError",
    "ToncenterNotFoundError",
    "ToncenterRetryError",
    "ToncenterServerError",
    "ToncenterSessionError",
    "ToncenterStatusError",
    "ToncenterStreamingError",
    "ToncenterTooManyRequestsError",
    "ToncenterUnauthorizedError",
    "ToncenterUnprocessableError",
    "ToncenterValidationError",
    "extract_error_message",
    "raise_for_status",
]


class ToncenterError(Exception):
    """Base exception for all TON Center errors."""

    message: str

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class ToncenterConnectionError(ToncenterError):
    """Network-level error (DNS failure, timeout, refused connection)."""


class ToncenterStatusError(ToncenterError):
    """API returned a non-2xx HTTP status."""

    status: int
    hint: t.ClassVar[str] = ""

    def __init__(self, *, status: int, message: str) -> None:
        self.status = status
        text = f"HTTP {status}: {message}"
        if self.hint:
            text += f" — {self.hint}"
        super().__init__(text)


class ToncenterClientError(ToncenterStatusError):
    """Client-side HTTP error (4xx)."""


class ToncenterServerError(ToncenterStatusError):
    """Server-side HTTP error (5xx)."""


class ToncenterBadRequestError(ToncenterClientError):
    """HTTP 400 Bad Request."""

    hint = "check query parameters, request body, and path arguments"


class ToncenterUnauthorizedError(ToncenterClientError):
    """HTTP 401 Unauthorized."""

    hint = "get a valid API key via @toncenter bot on Telegram"


class ToncenterForbiddenError(ToncenterClientError):
    """HTTP 403 Forbidden."""

    hint = "API key was issued for a different network (e.g. testnet key on mainnet)"


class ToncenterNotFoundError(ToncenterClientError):
    """HTTP 404 Not Found."""


class ToncenterMethodNotAllowedError(ToncenterClientError):
    """HTTP 405 Method Not Allowed."""

    hint = "use GET or POST"


class ToncenterConflictError(ToncenterClientError):
    """HTTP 409 Conflict."""

    hint = "resource found but does not match the expected type"


class ToncenterUnprocessableError(ToncenterClientError):
    """HTTP 422 Unprocessable Content."""

    hint = "check request parameters for missing, malformed, or conflicting values"


class ToncenterTooManyRequestsError(ToncenterClientError):
    """HTTP 429 Too Many Requests."""

    hint = "reduce request frequency or upgrade your plan"


class ToncenterInternalServerError(ToncenterServerError):
    """HTTP 500 Internal Server Error."""


class ToncenterGatewayTimeoutError(ToncenterServerError):
    """HTTP 504 Gateway Timeout."""

    hint = "liteserver did not respond in time, retry the request"


class ToncenterLiteServerError(ToncenterServerError):
    """HTTP 542 Server Error."""

    hint = "liteserver error or unsupported TVM stack type"


class ToncenterValidationError(ToncenterError):
    """Response body did not match the expected Pydantic model."""

    model: type
    errors: list[t.Any]

    def __init__(self, *, model: type, errors: list[t.Any]) -> None:
        self.model = model
        self.errors = errors
        field_hints = ", ".join(f"{e.get('loc', '?')}: {e.get('msg', '')}" for e in errors[:3])
        if len(errors) > 3:
            field_hints += f" ... (+{len(errors) - 3} more)"
        super().__init__(
            f"Response validation failed for {model.__name__}: {field_hints}",
        )


class ToncenterSessionError(ToncenterError):
    """Session was not created before making a request."""


class ToncenterStreamingError(ToncenterError):
    """Streaming transport error."""


class ToncenterConnectionLostError(ToncenterStreamingError):
    """Connection lost and reconnect limit exceeded."""

    attempts: int

    def __init__(self, *, attempts: int) -> None:
        self.attempts = attempts
        super().__init__(
            f"Connection lost after {attempts} reconnect attempts",
        )


class ToncenterRetryError(ToncenterError):
    """All retry attempts have been exhausted."""

    attempts: int
    last_status: int | None
    last_error: Exception | None

    def __init__(
        self,
        *,
        attempts: int,
        last_status: int | None = None,
        last_error: Exception | None = None,
    ) -> None:
        self.attempts = attempts
        self.last_status = last_status
        self.last_error = last_error
        parts = [f"Retry limit exceeded after {attempts} attempts"]
        if last_status is not None:
            parts.append(f"last status: {last_status}")
        if last_error is not None:
            parts.append(f"last error: {last_error}")
        super().__init__(", ".join(parts))


STREAMING_RECOVERABLE: t.Final[tuple[type[ToncenterError], ...]] = (
    ToncenterServerError,
    ToncenterStreamingError,
    ToncenterTooManyRequestsError,
)

TONCENTER_STATUS_TO_EXCEPTION: t.Final[dict[int, type[ToncenterStatusError]]] = {
    400: ToncenterBadRequestError,
    401: ToncenterUnauthorizedError,
    403: ToncenterForbiddenError,
    404: ToncenterNotFoundError,
    405: ToncenterMethodNotAllowedError,
    409: ToncenterConflictError,
    422: ToncenterUnprocessableError,
    429: ToncenterTooManyRequestsError,
    500: ToncenterInternalServerError,
    504: ToncenterGatewayTimeoutError,
    542: ToncenterLiteServerError,
}


def extract_error_message(body: str) -> str:
    """Extract a human-readable error message from a response body.

    :param body: Raw response text.
    :return: Error message string.
    """
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return body
    if isinstance(data, dict):
        message = data.get("error") or data.get("Error") or body
        return str(message)
    return str(data)


def raise_for_status(status: int, body: str, content_type: str = "") -> None:
    """Raise an appropriate exception for non-2xx HTTP status.

    :param status: HTTP status code.
    :param body: Response body text.
    :param content_type: Content-Type header value.
    :raises ToncenterStatusError: On any mapped HTTP error.
    """
    message = "Unexpected HTML response" if "text/html" in content_type else extract_error_message(body)

    exc_class = TONCENTER_STATUS_TO_EXCEPTION.get(status)
    if exc_class:
        raise exc_class(status=status, message=message)

    if 400 <= status < 500:
        raise ToncenterClientError(status=status, message=message)
    if 500 <= status < 600:
        raise ToncenterServerError(status=status, message=message)

    raise ToncenterError(f"HTTP {status}: {message}")
