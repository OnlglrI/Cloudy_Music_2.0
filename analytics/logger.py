import logging

logger = logging.getLogger("analytics_logger")
logger.setLevel(logging.INFO)

# формат логов
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# вывод в stdout
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)