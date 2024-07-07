from types import SimpleNamespace

class BaseConfig:
    select_hint_text: str
    size: str
    show_preview: bool
    preview_position: str
    preview_size: int
    preview_wrap_enabled: bool


class Configurator(type):
    def __new__(cls, name, bases, attrs):
        config_object = SimpleNamespace(**attrs)
        conf_attrs = {
            "select_hint_text": getattr(config_object, "select_hint_text", "Select configmap"),
            "size": getattr(config_object, "size", "30%"),
            "show_preview": getattr(config_object, "show_preview", True),
            "preview_position": getattr(config_object, "preview_position", "up"),
            "preview_wrap_enabled": getattr(config_object, "preview_wrap_enabled", True),
            "preview_size": getattr(config_object, "preview_size", 3),
        }
        return super().__new__(cls, name, bases, conf_attrs)


class MyCustomConfig(BaseConfig, metaclass=Configurator):
    select_hint_text = "Select configmap from the list"
    show_preview = True
    preview_position = "up"
    preview_size = 3
    preview_wrap_enabled = True
