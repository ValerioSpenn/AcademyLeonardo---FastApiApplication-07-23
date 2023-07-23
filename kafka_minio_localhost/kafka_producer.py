from confluent_kafka import Producer
from datetime import datetime
import json, time, sys, logging, random, copy, uuid


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
producer = Producer({
    'bootstrap.servers': endpoint
})
logger.info('Kafka Producer has been initiated...')
#################################################################################
def receipt(err,msg):
    if err is not None:
        message = 'Error: {}'.format(err)
    else:
        message = 'Produced message on topic {} with value of {}\n'.format(msg.topic(), msg.value().decode('utf-8'))
    logger.info(message)
#################################################################################
def main():
#    with open('message_template.json', 'r') as f_in:
#        message_template = json.load(f_in)
    for i in range(1):
#        msg = copy.deepcopy(message_template)

#{  
#      "victim_id": string,
#      "respiratory_rate": int,
#      "skin_temperature": double,
#      "heart_rate": int,
#      "image_id": {
#         "image_name": "vitals_victim_0.JPG",
#         "base_url": "http://nightingale.minio/tss/",
#        }
#       "position": {
#          "long": 33.22,
#          "lat": 10.3,
#          "alt": 20.35
#       },
#      "timestamp": "2021-02-10T15:04:47.149+00:00"
# }

        datetimeNOW = datetime.now()

        msg = {}
        msg['id'] = random.randint(1000, 2000)
        msg['type'] = random.choice(['Type1', 'Type2', 'Type3'])
        msg['dateObserved'] = {}
        msg['dateObserved']['type'] = "DateTime"
        msg['dateObserved']['value'] = datetimeNOW.strftime("%T-%m-%dT%H:%M:%S.%f%z")
        msg['payload'] = {}
        msg['payload']['victim_id'] = str(uuid.uuid4())
        msg['payload']['heart_rate'] = random.randint(60, 100) # 0 200
        msg['payload']['respiratory_rate'] = random.randint(12, 16) # 0 40
        msg['payload']['skin_temperature'] = round(random.uniform(36.5,37.2), 1) # 0 50
        msg['payload']['image_id'] = {} 
        msg['payload']['image_id']['image_name'] = "vitals_victim_0.JPG" 
        msg['payload']['image_id']['bucket_name'] = "tss-bucket-test"
        msg['payload']['image_id']['base_url'] = "http://nightingale.minio/tss/"
        msg['payload']['position'] = {}
        msg['payload']['position']['lat'] = round(random.uniform(-90, 90), 5)
        msg['payload']['position']['long'] = round(random.uniform(-180, 180), 5)
        msg['payload']['position']['alt'] = round(random.uniform(-1000, 1000), 5)
        msg['payload']['timestamp'] = datetimeNOW.strftime("%T-%m-%dT%H:%M:%S.%f%z")


#        logger.info(msg)

        payload = json.dumps(msg).encode('utf-8')

        producer.poll(1.)
        producer.produce(topic=TOPIC,
                         value=payload,
                         callback=receipt)
        producer.flush()

        time.sleep(.500)


if __name__ == '__main__':
    main()
