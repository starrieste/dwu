import os
from platformdirs import user_config_dir

import tomllib
import tomli_w

class Config:
    def __init__(self):
        self._config_file = os.path.join(
            user_config_dir("dwu"),
            "config.toml"
        )
        os.makedirs(os.path.dirname(self._config_file), exist_ok=True)
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self._config_file):
            return {}

        try:
            with open(self._config_file, "rb") as f:
                return tomllib.load(f)
        except tomllib.TOMLDecodeError:
            return {}

    def _save(self):
        with open(self._config_file, "wb") as f:
            tomli_w.dump(self.data, f)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self._save()
