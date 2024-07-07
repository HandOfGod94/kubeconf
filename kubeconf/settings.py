from kubeconf import BaseConfig


class DefaultSettings(BaseConfig):
    select_hint_text = "Select a configmap"
    size = "30%"
    show_preview = True
    preview_position = "up"
    preview_size = 3


app_settings = [DefaultSettings]


def KubeconfSettings(cls):
    """
    Settings registration decorator for your custom config class.

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
    @OverrideSettings
    class MyCustomSettings():
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
    global app_settings
    app_settings.append(cls)

    def wrapper(*args, **kwargs):
        return cls(BaseConfig, *args, **kwargs)

    return wrapper
