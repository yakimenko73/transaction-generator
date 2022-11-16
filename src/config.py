from datetime import datetime
from logging import _nameToLevel as valid_log_levels
from typing import Final, Any

import yaml
from loguru import logger
from pydantic.class_validators import validator
from pydantic.main import BaseModel

CONFIG_PATH: Final[str] = '../config/config.yaml'


class AppConfig(BaseModel):
    csv_path: str


class LoggerConfig(BaseModel):
    level: str
    file_path: str

    @validator('level')
    @classmethod
    def is_valid_log_level(cls, level: str) -> str:
        if level not in valid_log_levels:
            raise ValueError(f'Invalid log level. Expected: {valid_log_levels}')
        return level


class IdGeneratorConfig(BaseModel):
    seed: int


class DateGeneratorConfig(BaseModel):
    start_date: datetime


class GeneratorsConfig(BaseModel):
    id_generator: IdGeneratorConfig
    date_generator: DateGeneratorConfig


class Config(BaseModel):
    app: AppConfig
    generators: GeneratorsConfig
    logger: LoggerConfig

    @classmethod
    def load(cls) -> Any:
        try:
            with open(CONFIG_PATH, 'r') as f:
                yml = yaml.safe_load(f)
        except FileNotFoundError as ex:
            logger.error(ex)
            raise ex

        return cls(**yml)

    def configure_logger(self):
        logger.add(self.logger.file_path, level=self.logger.level)
