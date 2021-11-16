import os
import json


class TickerConfig:
    CONFIG = "config.json"

    def __init__(self):
        self.all_config = {}
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.base_dir, self.CONFIG)

    def get_config(self):
        with open(self.config_path) as f:
            self.all_config = json.load(f)
        return self.all_config
