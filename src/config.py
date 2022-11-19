from datetime import datetime
from logging import _nameToLevel as valid_log_levels
from typing import Final, Any

import yaml
from loguru import logger
from pydantic.class_validators import validator
from pydantic.main import BaseModel

from utils import percentage_off

CONFIG_PATH: Final[str] = './config/config.yaml'


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
    start: int
    stop: int


class PxFillConfig(BaseModel):
    rounding: int
    start: float
    stop: float


class VolumeInitConfig(BaseModel):
    rounding: int
    start: int
    stop: int


class DateGeneratorConfig(BaseModel):
    start_date: datetime
    start: int
    stop: int


class GeneratorConfig(BaseModel):
    max_orders: int
    percent_completed_orders: int
    percent_created_and_completed_orders: int
    percent_created_orders: int
    id_generator: IdGeneratorConfig
    px_fill_generator: PxFillConfig
    volume_init_generator: VolumeInitConfig
    date_generator: DateGeneratorConfig

    def segment_size(self, segment_percent: int) -> int:
        return int(percentage_off(self.max_orders, segment_percent))

    def first_two_segments_size(self) -> int:
        return self.segment_size(self.percent_completed_orders + self.percent_created_and_completed_orders)


class Config(BaseModel):
    app: AppConfig
    generator: GeneratorConfig
    logger: LoggerConfig

    @classmethod
    def load(cls) -> Any:
        logger.debug(f'Trying to load config from {CONFIG_PATH}')

        try:
            with open(CONFIG_PATH, 'r') as f:
                yml = yaml.safe_load(f)
        except FileNotFoundError as ex:
            logger.error(ex)
            raise ex

        logger.debug('Application configured successfully')

        return cls(**yml)

    def configure_logger(self) -> None:
        logger.add(self.logger.file_path, level=self.logger.level)
