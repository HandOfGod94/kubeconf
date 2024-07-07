from subprocess import check_output
from .fzf_input import fzf_input
import json
import logging


class Searcher:
    def __init__(self, config):
        self.config = config
        self.current_namespace = (
            check_output("kubectl config view --minify -o jsonpath='{..namespace}'", shell=True).strip().decode("utf-8")
        )

    def configmaps(self):
        return (
            check_output("kubectl get configmaps | tail -n +2 | awk '{print $1}'", shell=True)
            .strip()
            .decode("utf-8")
            .splitlines()
        )

    def lookup_config(self, selected_configmap):
        configmap = (
            check_output(f"kubectl get configmap -n {self.current_namespace} -o json {selected_configmap}", shell=True)
            .strip()
            .decode("utf-8")
        )
        configmap = json.loads(configmap)
        key = fzf_input(
            configmap["data"].keys(),
            height=self.config.size,
            header=f"Searching in {selected_configmap} of {self.current_namespace}",
            preview=f"echo '{json.dumps(configmap['data'])}' | jq  --raw-output '.{{}}'",
            position=f"{self.config.preview_position}:{self.config.preview_size}:wrap",
        )

        logging.info(f"Searched in {selected_configmap} of {self.current_namespace}")
        print(json.dumps({key: configmap["data"][key]}, indent=2))

    def execute(self):
        selected_configmap = fzf_input(self.configmaps(), height=self.config.size, header=self.config.select_hint_text)

        self.lookup_config(selected_configmap)
