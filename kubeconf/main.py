import argparse
import importlib.machinery
import os

from kubeconf import __version__

from .searcher import Searcher
from .settings import app_settings

parser = argparse.ArgumentParser(prog="kubeconf", description="Search for kubernetes configmap")
parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")


def user_settings_path():
    config_dir = os.getenv("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"))
    filename = "kubeconf_settings" if os.getenv("XDG_CONFIG_HOME") else ".kubeconf_settings"
    config_path = os.path.join(config_dir, filename)
    if os.path.exists(config_path):
        return config_path


def main():
    parser.parse_args()

    overrides = user_settings_path()
    if overrides:
        importlib.machinery.SourceFileLoader("user_settings", user_settings_path()).load_module()

    config = app_settings[-1]()  # get the last loaded settings from decorator
    Searcher(config).execute()


if __name__ == "__main__":
    main()
