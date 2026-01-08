from plugins.console import ConsoleLogger
class PluginManager:
    def __init__(self):
        self.plugins = {}
        # Auto-register our console logger for now
        # In a real app, this would be dynamic!
        self.register(ConsoleLogger())
    def register(self, plugin):
        self.plugins[plugin.slug] = plugin
        plugin.enable()
        print(f"Registered plugin: {plugin.slug}")
    def get_plugin(self, slug):
        return self.plugins.get(slug)
    def get_all_by_type(self, plugin_type):
        return [p for p in self.plugins.values() if getattr(p, "type", None) == plugin_type]
# Singleton instance
manager = PluginManager()