import pika
import json
import logging
from configparser import ConfigParser

class RabbitMQPublisher:

    # Configuração do logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, config_file):

        self.config = ConfigParser()
        self.config.read(config_file)
        
        credentials = pika.PlainCredentials(
            self.config['RABBITMQ']['RABBIT_USER'], self.config['RABBITMQ']['RABBIT_PASS']
        )
        
        self.connection_parameters = pika.connection.ConnectionParameters(
            self.config['RABBITMQ']['RABBIT_HOST'],
            self.config['RABBITMQ']['RABBIT_PORT'],
            self.config['RABBITMQ']['RABBIT_VHOST'],
            credentials
        )

        self.rabbit_queue = self.config['RABBITMQ']['RABBIT_WRITE_IN']

    def send(self, body):
        with pika.BlockingConnection(self.connection_parameters) as connection:
            channel = connection.channel()
            channel.basic_qos(prefetch_count=1)
            
            body_str = json.dumps(body)
            
            try:
                channel.basic_publish(
                    exchange='',
                    routing_key=self.rabbit_queue,
                    body=body_str
                )
                logging.info(f"Sent message: {body_str}")
            except Exception as e:
                logging.error(f"Error publishing message: {e}")