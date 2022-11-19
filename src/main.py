from typing import List

from hurry.filesize import size
from loguru import logger

from src.config import Config, GeneratorsConfig
from src.order.book import FiatOrderBook
from src.order.builder import PseudoRandomFiatOrderBuilder
from src.order.domain.domain import Order
from src.order.storage import ArrayStorage, CsvFileStorage


def generate_orders(config: GeneratorsConfig) -> List[Order]:
    storage = ArrayStorage()
    order_book = FiatOrderBook(config, storage)
    order_builder = PseudoRandomFiatOrderBuilder(config)
    for i in range(config.max_orders):
        order = order_builder.build()
        order_book.add(order)

    logger.info(f'Order book contains {order_book.size} generated orders')

    return storage.find_all()


def workflow(config: Config) -> None:
    orders = generate_orders(config.generators)

    with CsvFileStorage(config.app.csv_path) as storage:
        storage.write(orders)

    logger.info(f'Flushed order history log to csv file. Size: {size(storage.size())}')


if __name__ == "__main__":
    cfg: Config = Config.load()
    cfg.configure_logger()

    workflow(cfg)
