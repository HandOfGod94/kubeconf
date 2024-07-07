from .searcher import Searcher
from .settings import MyCustomSettings

config = MyCustomSettings()
Searcher(config).execute()
