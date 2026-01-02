from typing import Any, Callable
import inspect

from licenscope.core.errors import ConfigError
from licenscope.sources.certificate import CertificateSource
from licenscope.sources.file import FileSource
from licenscope.sources.url import UrlSource


SOURCE_FACTORIES: dict[str, Callable[..., Any]] = {
    CertificateSource.kind: CertificateSource,
    FileSource.kind: FileSource,
    UrlSource.kind: UrlSource,
}


def create_source(kind: str, **kwargs):
    factory = SOURCE_FACTORIES.get(kind)
    if factory is None:
        raise ConfigError(f"Unknown source kind: {kind}")
    params = inspect.signature(factory).parameters
    filtered = {key: value for key, value in kwargs.items() if key in params}
    return factory(**filtered)
