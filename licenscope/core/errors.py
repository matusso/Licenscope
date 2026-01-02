class LicenscopeError(Exception):
    """Base error for Licenscope."""


class ConfigError(LicenscopeError):
    """Raised when configuration is invalid."""


class ParserError(LicenscopeError):
    """Raised when parsing fails."""


class SourceError(LicenscopeError):
    """Raised when loading a source fails."""
