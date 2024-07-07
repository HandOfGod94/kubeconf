from kubeconf.config import BaseSettings


class MyCustomSettings(BaseSettings):
    select_hint_text = "Select a configmap"
    size = "30%"
    show_preview = True
    preview_position = "up"
    preview_size = 5
