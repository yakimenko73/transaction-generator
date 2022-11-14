from datetime import datetime

from pydantic.main import BaseModel


class IdGeneratorConfig(BaseModel):
    modulus: int
    multiplier: int
    increment: int
    seed: int


class SideGeneratorConfig(BaseModel):
    modulus: int
    multiplier: int
    increment: int


class InstrumentGeneratorConfig(BaseModel):
    modulus: int
    multiplier: int
    increment: int


class StatusGeneratorConfig(BaseModel):
    modulus: int
    multiplier: int
    increment: int


class PxFillGeneratorConfig(BaseModel):
    modulus: float
    multiplier: float
    increment: float


class VolumeInitGeneratorConfig(BaseModel):
    modulus: int
    multiplier: int
    increment: int
    seed: int


class VolumeFillGeneratorConfig(BaseModel):
    multiplier: int
    increment: int


class DateGeneratorConfig(BaseModel):
    modulus: int
    multiplier: int
    increment: int
    seed: int
    start_date: datetime


class NoteGeneratorConfig(BaseModel):
    modulus: int
    multiplier: int
    increment: int


class TagGeneratorConfig(BaseModel):
    seed: int
    num_modulus: int
    num_multiplier: int
    num_increment: int
    tag_modulus: int
    tag_multiplier: int
    tag_increment: int


class GeneratorsConfig(BaseModel):
    id_generator: IdGeneratorConfig
    side_generator: SideGeneratorConfig
    instrument_generator: InstrumentGeneratorConfig
    status_generator: StatusGeneratorConfig
    px_fill_generator: PxFillGeneratorConfig
    volume_init_generator: VolumeInitGeneratorConfig
    volume_fill_generator: VolumeFillGeneratorConfig
    date_generator: DateGeneratorConfig
    note_generator: NoteGeneratorConfig
    tag_generator: TagGeneratorConfig
