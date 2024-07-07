import kubeconf


class MyCustomSettings(kubeconf.BaseSettings):
    @staticmethod
    def calculated_size():
        return "30%"

    select_hint_text = "Select a configmap"
    size = calculated_size
    show_preview = lambda: False  # or it can even be a lambda
    preview_position = "up"
    preview_size = 3
