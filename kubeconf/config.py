from types import SimpleNamespace
from typing import Callable, Literal


class KubeconfSettings(type):
    def __new__(cls, name, bases, attrs):
        config_object = SimpleNamespace(**attrs)
        conf_attrs = {
            "select_hint_text": getattr(config_object, "select_hint_text", "Select configmap"),
            "size": getattr(config_object, "size", "30%"),
            "show_preview": getattr(config_object, "show_preview", True),
            "preview_position": getattr(config_object, "preview_position", "up"),
            "preview_size": getattr(config_object, "preview_size", 3),
        }
        conf_attrs = {k: v() if callable(v) else v for k, v in conf_attrs.items()}
        return super().__new__(cls, name, bases, conf_attrs)


class BaseSettings(metaclass=KubeconfSettings):
    """
    Base settings class for kubeconf. This class should be inherited by the user's custom settings class.

    Attributes:
        select_hint_text (str | Callable[[], str] ): The hint text to show on fzf prompts. E.g. "Select a configmap"
        size (str | Callable[[], str]): The size of the whole fzf window. E.g. "30%" or "20%"
        show_preview (bool | Callable[[], bool]): Whether to show the fzf preview window or not.
        preview_position (str | Callable[[], str]): The position of the fzf preview window (up, down, left, right)
        preview_size (int | Callable[[], int]): The size of the preview window. e.g. (1,2,3,4,50)

    These attributes can be callable functions that return the desired value. This is useful when the value needs to be
    calculated at runtime. For example, the `size` attribute can be a function that returns the size based on the screen.

    Example:

    ```python
    class MyCustomSettings(kubeconf.BaseSettings):
        @staticmethod
        def calculated_size():
            return "30%"

        select_hint_text = "Select a configmap"
        size = calculated_size
        show_preview = lambda: True # or it can even be a lambda
        preview_position = "up"
        preview_size = 3
    ```
    """

    select_hint_text: str | Callable[[], str]
    """The hint text to show on fzf prompts. E.g. "Select a configmap" """

    size: str | Callable[[], str]
    """The size of the whole fzf window. E.g. "30%" or "20%" """

    show_preview: bool | Callable[[], bool]
    """Whether to show the fzf preview window or not."""

    preview_position: Literal["up", "down", "left", "right"] | Callable[[], Literal["up", "down", "left", "right"]]
    """The position of the fzf preview window (up, down, left, right)"""

    preview_size: int | Callable[[], int]
    """The size of the preview window. e.g. (1,2,3,4,50) """
