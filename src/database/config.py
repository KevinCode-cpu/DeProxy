import os
from pathlib import Path

import streamlit as st

try:
    from supabase import Client, create_client
except Exception as exc:
    Client = None  # type: ignore[assignment]
    create_client = None  # type: ignore[assignment]
    SUPABASE_IMPORT_ERROR = exc
else:
    SUPABASE_IMPORT_ERROR = None


def _load_local_secrets() -> dict:
    """Load secrets from the common Streamlit and project-local locations."""
    candidates = [Path(".streamlit/secrets.toml"), Path("streamlit/secrets.toml")]
    for candidate in candidates:
        if not candidate.exists():
            continue
        try:
            import tomllib

            with candidate.open("rb") as fh:
                data = tomllib.load(fh)
            if isinstance(data, dict):
                return {str(k): str(v) for k, v in data.items()}
        except Exception:
            continue
    return {}


def _get_secret(key: str) -> str:
    """Read from Streamlit secrets, then fall back to env vars and local files."""
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass

    env_value = os.getenv(key, "")
    if env_value:
        return env_value

    local_secrets = _load_local_secrets()
    return str(local_secrets.get(key, ""))


def _is_placeholder_value(value: str | None) -> bool:
    if value is None:
        return True

    cleaned = value.strip()
    if not cleaned:
        return True

    normalized = cleaned.lower()
    placeholder_signals = (
        "paste_",
        "your_",
        "replace_me",
        "changeme",
        "example.com",
        "dummy",
        "mock",
        "placeholder",
        "<your",
        "<paste",
    )
    return any(signal in normalized for signal in placeholder_signals)


SUPABASE_URL = _get_secret("SUPABASE_URL")
SUPABASE_SECRET_KEY = _get_secret("SUPABASE_SECRET_KEY")

# Create the client only when we actually have valid credentials.
if (
    SUPABASE_IMPORT_ERROR is None
    and SUPABASE_URL
    and SUPABASE_SECRET_KEY
    and create_client
    and not _is_placeholder_value(SUPABASE_URL)
    and not _is_placeholder_value(SUPABASE_SECRET_KEY)
):
    supabase = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)
else:
    # Keep app importable; screens can surface a friendly error.
    supabase = None
