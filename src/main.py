from loguru import logger

from src.config import Config
from src.order.book import FiatOrderBook
from src.order.storage import ArrayStorage


def workflow(config: Config):
    order_book = FiatOrderBook(config)
    storage = ArrayStorage()
    for i in range(7200):
        order = order_book.get_last_order()
        storage.add(order)
        logger.info(storage.find_by_id(order.id))


if __name__ == "__main__":
    cfg: Config = Config.load()
    cfg.configure_logger()

    workflow(cfg)
