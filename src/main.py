from loguru import logger

from src.config import Config
from src.order.book import FiatOrderBook
from src.order.builder import PseudoRandomFiatOrderBuilder
from src.order.storage import ArrayStorage


def workflow(config: Config) -> None:
    storage = ArrayStorage()
    order_book = FiatOrderBook(config.generators, storage)
    order_builder = PseudoRandomFiatOrderBuilder(config.generators)
    for i in range(config.generators.max_orders):
        order = order_builder.build()
        order_book.add(order)

    logger.info(f'Order book contains {order_book.size} generated orders')


if __name__ == "__main__":
    cfg: Config = Config.load()
    cfg.configure_logger()

    workflow(cfg)
