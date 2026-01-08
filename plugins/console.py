from .base import NotificationPlugin
import time

class ConsoleLogger(NotificationPlugin):
    slug = "console-logger"
    def enable(self):
        print(f"[{self.slug}] Plugin enabled")
    def disable(self):
        print(f"[{self.slug}] Plugin disabled")
    def send(self, message: str, targets: list):
        print(f"[{self.slug}] Sending to {targets}...")
        time.sleep(5) # SIMULATE SLOW NETWORK CALL
        print(f"[{self.slug}] Sent: {message}")