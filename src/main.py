from hurry.filesize import size
from loguru import logger
from typing import List, Final

from config import Config, GeneratorConfig
from orders.book import FiatOrderBook
from orders.builder import PseudoRandomFiatOrderBuilder
from orders.domain.domain import Order
from orders.storage import ArrayStorage, CsvFileStorage

CONFIG_PATH: Final[str] = '../config/config.yaml'


def generate_orders(config: GeneratorConfig) -> List[Order]:
    storage = ArrayStorage()
    order_book = FiatOrderBook(config, storage)
    order_builder = PseudoRandomFiatOrderBuilder(config)
    for i in range(config.max_orders):
        order = order_builder.build()
        order_book.add(order)

    logger.info(f'Order book contains {order_book.size} generated orders')

    return storage.find_all()


def workflow(config: Config) -> None:
    orders = generate_orders(config.generator)

    with CsvFileStorage(config.app.csv_path) as storage:
        storage.write(orders)

    logger.info(f'Flushed order history log to csv file. Size: {size(storage.size())}')


if __name__ == "__main__":
    cfg: Config = Config.load(CONFIG_PATH)
    cfg.configure_logger()

    workflow(cfg)
