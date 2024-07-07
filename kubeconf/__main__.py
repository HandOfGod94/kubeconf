from .searcher import Searcher
from .config import MyCustomConfig

config = MyCustomConfig()
Searcher(config).execute()
