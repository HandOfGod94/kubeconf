import argparse
import json
import logging
from subprocess import check_output

from kubeconf import __version__

from .fzf_input import fzf_input

parser = argparse.ArgumentParser(prog="kubeconf", description="Interactively lookup in kubernetes configmap")
parser.add_argument("-n", "--namespace", help="Namespace to search in. Default is current namespace")
parser.add_argument("-s", "--size", help="Size of the fzf window. Default: 30%%", default="30%")
parser.add_argument(
    "-pp",
    "--preview-position",
    help="Preview window position. Default: up",
    default="up",
    choices=["up", "down", "left", "right"],
)
parser.add_argument("-ps", "--preview-size", help="Preview window size (in terminal lines). Default: 3", default=3)
parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")


class KubeconfSearcher:
    def __init__(self, options):
        self.namespace = options.namespace or self._current_namespace()
        self.size = options.size
        self.preview_position = options.preview_position
        self.preview_size = options.preview_size

    def _current_namespace(self):
        return (
            check_output("kubectl config view --minify -o jsonpath='{..namespace}'", shell=True).strip().decode("utf-8")
        )

    def configmaps(self):
        return (
            check_output(f"kubectl get configmaps -n {self.namespace} | tail -n +2 | awk '{{print $1}}'", shell=True)
            .strip()
            .decode("utf-8")
            .splitlines()
        )

    def execute(self):
        selected_configmap = fzf_input(self.configmaps(), height=self.size, header=f"Select a configmap in namespace: {self.namespace}")
        if not selected_configmap or selected_configmap == "":
            return

        configmap = (
            check_output(f"kubectl get configmap -n {self.namespace} -o json {selected_configmap}", shell=True)
            .strip()
            .decode("utf-8")
        )
        configmap = json.loads(configmap)
        key = fzf_input(
            configmap["data"].keys(),
            height=self.size,
            header=f"Searching in {selected_configmap} of {self.namespace}",
            preview=(f"echo '{json.dumps(configmap['data'])}' | jq  --raw-output '.{{}}'"),
            position=f"{self.preview_position}:{self.preview_size}:wrap",
        )

        logging.info(f"Searched in {selected_configmap} of {self.namespace}")
        try:
            print(json.dumps({key: configmap["data"][key]}, indent=2))
        except KeyError:
            print(configmap['data'][key]) if key in configmap['data'] else print("")


def execute():
    KubeconfSearcher(parser.parse_args()).execute()
