import importlib.machinery

from .searcher import Searcher
from .settings import app_settings

user_settings = importlib.machinery.SourceFileLoader("user_settings", "examples/kubeconf_settings").load_module()

config = app_settings[-1]()  # get the last loaded settings from decorator
Searcher(config).execute()
