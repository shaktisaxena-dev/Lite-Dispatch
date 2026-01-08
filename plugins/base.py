from abc import ABC, abstractmethod
from pydantic import BaseModel
# Schema for what a plugin needs to resolve (just common settings for now)
class PluginConfig(BaseModel):
    enabled: bool = True
class BasePlugin(ABC):
    slug: str = "base-plugin"
    @abstractmethod
    def enable(self):
        """Called when plugin is enabled"""
        pass
    @abstractmethod
    def disable(self):
        """Called when plugin is disabled"""
        pass
class NotificationPlugin(BasePlugin):
    """
    Specific contract for plugins that send messages.
    """
    type: str = "notification"
    @abstractmethod
    def send(self, message: str, targets: list):
        """
        Send a message to a list of targets (emails, slack channels, etc.)
        """
        pass