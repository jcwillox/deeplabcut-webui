import argparse
import os
from functools import lru_cache
from typing import Optional, Dict, Any, Tuple

import yaml
from pydantic import BaseSettings, Field
from pydantic.env_settings import SettingsSourceCallable
from pydantic.fields import ModelField


class Settings(BaseSettings):
    projects: str = Field(
        default="backend/tests/testdata",
        description="path to directory containing your DLC projects",
        metavar="PATH",
    )
    frame_format: str = Field(
        default="img{:04}.png",
        description="formatting string for the name of extracted frames (default: img{:04}.png)",
        metavar="FORMAT",
    )
    host: str = Field(
        default="127.0.0.1",
        description="bind the server to this address (default: 127.0.0.1)",
    )
    port: int = Field(
        default=8000,
        description="bind the server to this port (default: 8000)",
    )
    token: Optional[str] = Field(
        description="token used to secure the backend from unauthorised access",
    )
    ssl_certfile: Optional[str] = Field(
        description="path to SSL certificate",
        metavar="PATH",
    )
    ssl_keyfile: Optional[str] = Field(
        description="path to SSL certificates private key",
        metavar="PATH",
    )

    class Config:
        env_file = ".env"
        env_prefix = "dlc_"
        secrets_dir = "/run/secrets"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            def cmdline_arguments(settings: BaseSettings) -> Dict[str, Any]:
                parser = argparse.ArgumentParser(prog="dlc-webui")

                for field in settings.__fields__.values():
                    field: ModelField
                    parser.add_argument(
                        "--" + field.name.replace("_", "-"),
                        type=field.type_,
                        required=field.required,
                        metavar=field.field_info.extra.get("metavar"),
                        help=field.field_info.description,
                    )

                args, _ = parser.parse_known_args()
                return {k: v for k, v in vars(args).items() if v is not None}

            def yaml_config(_) -> Dict[str, Any]:
                def find_config():
                    path = os.path.expanduser("~/.config/dlc-webui/config.yaml")
                    if os.path.exists(path):
                        return path
                    path = os.getcwd()
                    while path.count(os.path.sep) > 1:
                        filepath = os.path.join(path, ".dlc-webui.yaml")
                        if os.path.exists(filepath):
                            return filepath
                        path = os.path.dirname(path)
                    return None

                config_path = find_config()
                if config_path:
                    with open(config_path) as file:
                        return yaml.safe_load(file)
                return {}

            return (
                init_settings,
                cmdline_arguments,
                yaml_config,
                env_settings,
                file_secret_settings,
            )


@lru_cache()
def get_settings():
    return Settings()
