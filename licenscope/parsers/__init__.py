from licenscope.parsers.jinja_parser import JinjaParser
from licenscope.parsers.json_parser import JsonParser
from licenscope.parsers.regex_parser import RegexParser
from licenscope.parsers.registry import ParserRegistry


def build_registry() -> ParserRegistry:
    registry = ParserRegistry()
    registry.register(JinjaParser)
    registry.register(JsonParser)
    registry.register(RegexParser)
    return registry
