import json
import logging
from api.consumer import WebScraping
from api.SendQueue import RabbitMQPublisher
from utils.utils import book_to_dict

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

config_path = './config/config.ini'
logging.info(f"Loading configuration from: {config_path}")

# Crie a instancia do producer
publisher = RabbitMQPublisher(config_path)

try:
    for book_instance in WebScraping.get_book():
        try:
            book_json = json.dumps(book_to_dict(book_instance), ensure_ascii=False)
            publisher.send(book_json)
            logging.info(f"Book {book_instance.title} sent to the queue.")
        except Exception as e:
            logging.error(f"Error processing book {book_instance.title}. Reason: {e}")
except Exception as e:
    logging.error(f"Error fetching books. Reason: {e}")
