from confluent_kafka import Consumer
import sys, logging, json


HOST = "localhost"
PORT = 9092
TOPIC = "nightingale.tss.vitals"
#TOPIC = "my-topic1"
#################################################################################
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
#    filename='producer.log',
#    filemode='w'
#)
logger = logging.getLogger()
#logger.setLevel(logging.INFO)
#################################################################################
endpoint = f"{HOST}:{PORT}"
consumer=Consumer({
    'bootstrap.servers': endpoint,
    'group.id': 'python-consumer',
    'auto.offset.reset': 'earliest'
})
logger.info('Kafka Consumer has been initiated...')
#################################################################################
logger.info(f"Available topics to consume: {consumer.list_topics().topics.keys()}")
consumer.subscribe([TOPIC])
#################################################################################
def main():
    try:
        while True:
            msg = consumer.poll(timeout=1.) # timeout
            if msg is None:
                continue
            if msg.error():
                logger.error('Error: {}'.format(msg.error()))
                continue
            data = msg.value().decode('utf-8')
            logger.info(f"Message received: {data}")
    except KeyboardInterrupt:
        # Close down consumer to commit final offsets.
        consumer.close()
        logger.info('KeyboardInterrupt')    


if __name__ == '__main__':
    main()
