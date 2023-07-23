import os, sys, logging, json, io
from aws import aws


BUCKET_NAME = "tss-bucket-test"
OBJECT_NAME = "vitals_victim_0.jpg"
INPUT_FILE = "test_file.png"


### VPN
ENDPOINT_URL          = "http://localhost:9000"
AWS_ACCESS_KEY_ID     = "minio-root-user"
AWS_SECRET_ACCESS_KEY = "minio-root-password"

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
if __name__=='__main__':
    # MinIO endpoint and credentials
    endpoint_url = os.getenv('endpoint_url', ENDPOINT_URL)
    aws_access_key_id = os.getenv('aws_access_key_id', AWS_ACCESS_KEY_ID)
    aws_secret_access_key = os.getenv('aws_secret_access_key', AWS_SECRET_ACCESS_KEY)
    signature_version =  os.getenv('signature_version', 's3v4')
#    region_name = os.getenv(region_name, 'eu-west-1')

    aws = aws(endpoint_url=endpoint_url,
              aws_access_key_id=aws_access_key_id,
              aws_secret_access_key=aws_secret_access_key,
              signature_version=signature_version)
#    s3_resource = boto3.resource(...)
    s3_client = aws.create_client()
#################################################################################
    # create bucket
    aws.create_bucket(BUCKET_NAME, None)
#################################################################################
    # list buckets
    list_of_buckets = aws.list_buckets()
    logger.info(f"List of buckets: {list_of_buckets}")
#################################################################################
    # list objects in bucket {BUCKET_NAME}
    list_of_objects_in_bucket = aws.list_objects_in_bucket(BUCKET_NAME)
    logger.info(f"List of objects in bucket {BUCKET_NAME}: {list_of_objects_in_bucket}")
#################################################################################
    # upload file in bucket {BUCKET_NAME}
    additional_info = {
      'bucket_name': BUCKET_NAME,
      'object_name': OBJECT_NAME,
      'metadata': {
            'key1': 'value1'
        }
    }
    with open(INPUT_FILE, 'rb') as fileobj:
        aws.upload_file(fileobj, additional_info)
#################################################################################
    # list objects in bucket {BUCKET_NAME}
    list_of_objects_in_bucket = aws.list_objects_in_bucket(BUCKET_NAME)
    logger.info(f"List of objects in bucket {BUCKET_NAME}: {list_of_objects_in_bucket}")
#################################################################################
    # retrieve medatata
#    print(s3_client.head_object(Bucket=BUCKET_NAME, Key="test_file")['Metadata'])
#################################################################################
#################################################################################
#################################################################################
