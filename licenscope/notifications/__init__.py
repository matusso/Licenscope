from licenscope.notifications.opsgenie import OpsgenieNotifier
from licenscope.notifications.pagerduty import PagerDutyNotifier
from licenscope.notifications.registry import NotificationRegistry
from licenscope.notifications.slack import SlackNotifier


def build_registry() -> NotificationRegistry:
    registry = NotificationRegistry()
    registry.register(SlackNotifier)
    registry.register(OpsgenieNotifier)
    registry.register(PagerDutyNotifier)
    return registry
