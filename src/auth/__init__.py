from src.auth import service

# Explicitly state that 'service' is part of the public API of the 'auth' package.
# This satisfies Ruff F401 and is good practice for package structure.
__all__ = ["service"]
