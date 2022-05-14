from dataclasses import dataclass
import elasticapm
from loguru import logger

is_apm_setup = False


@dataclass
class APMConfig:
    url: str
    token: str
    environment: str

    def to_config_dict(self):
        return {
            "server_url": self.url,
            "secret_token": self.token,
            "environment": self.environment,
        }


def setup_apm_agent(service_name: str, config: APMConfig):
    global is_apm_setup
    if is_apm_setup:
        return

    apm_config_dict = {"service_name": service_name, **config.to_config_dict()}

    logger.info(f"APM config: { apm_config_dict }")

    # register singleton for `elasticapm.getClient`
    elasticapm.Client(**apm_config_dict)
    elasticapm.instrument()
    is_apm_setup = True
