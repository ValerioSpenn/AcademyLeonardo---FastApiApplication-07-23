import boto3, logging, io, json
from botocore.client import Config
from botocore.exceptions import ClientError


class aws():
    def __init__(self, 
                 endpoint_url, 
                 aws_access_key_id, 
                 aws_secret_access_key, 
                 signature_version, 
                 region_name=None):
        self.endpoint_url = endpoint_url
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.signature_version = signature_version
        self.region_name = region_name
        self.s3_client = None
################################################################################
    def create_client(self):
    
        try:
            if self.region_name is None:
                self.s3_client = boto3.client('s3',
                                              endpoint_url=self.endpoint_url,
                                              aws_access_key_id=self.aws_access_key_id,
                                              aws_secret_access_key=self.aws_secret_access_key,
                                              config=Config(signature_version=self.signature_version))
            else:
                self.s3_client = boto3.client('s3',
                                              endpoint_url=self.endpoint_url,
                                              aws_access_key_id=self.aws_access_key_id,
                                              aws_secret_access_key=self.aws_secret_access_key,
                                              config=Config(signature_version=self.signature_version),
                                              region_name=self.region_name)
        except ClientError as e:
            logging.error(e)
            return None
        return self.s3_client
################################################################################
    def create_bucket(self,bucket_name,region=None):
        """Create an S3 bucket in a specified region
    
        If a region is not specified, the bucket is created in the S3 default
        region (us-east-1).
    
        :param bucket_name: Bucket to create
        :param region: String region to create bucket in, e.g., 'us-west-2'
        :return: True if bucket created, else False
        """
    
        try:
            if region is None:
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': region}
                self.s3_client.create_bucket(Bucket=bucket_name,
                                             CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True
################################################################################
    def list_buckets(self):
        # Retrieve the list of existing buckets and output the bucket names
        s3_response = self.s3_client.list_buckets()
        list_of_buckets = [ bucket['Name'] for bucket in s3_response['Buckets'] ]
    
        return list_of_buckets
#################################################################################
    def list_objects_in_bucket(self, bucket_name):
        # retrieving the list of objects in bucket '{bucket_name}'
        s3_response = self.s3_client.list_buckets()
        list_of_buckets = [ bucket['Name'] for bucket in s3_response['Buckets'] ]
    
        if bucket_name in list_of_buckets:
            s3_response = self.s3_client.list_objects(Bucket=bucket_name)
            list_of_objects = []
            if 'Contents' in s3_response:
                list_of_objects = [ key['Key'] for key in s3_response['Contents'] ]
    
            return list_of_objects
        else:
            # bucket '{bucket_name}' doesn't exist
    
            return None
#################################################################################
    def upload_file(self, file, additional_info):
        bucket_name = additional_info['bucket_name']
        object_name = additional_info['object_name']
        metadata = {
            'Metadata': additional_info['metadata']
        }
    
#        logger.info(f"Uploading object '{object_name}' in bucket '{bucket_name}' with metadata '{metadata}'")

        s3_response = self.s3_client.list_buckets()
        list_of_buckets = [ bucket['Name'] for bucket in s3_response['Buckets'] ]
    
        if bucket_name in list_of_buckets:
            self.s3_client.upload_fileobj(Fileobj=file,
                                          Bucket=bucket_name,
                                          Key=object_name,
                                          ExtraArgs=metadata)
### Fileobj (bytes) vs Filename (string of file path)
#            self.s3_client.upload_fileobj(Filename=file,
#                                          Bucket=bucket_name,
#                                          Key=object_name,
#                                          ExtraArgs=metadata)
    
            return True
        else:
            # bucket '{bucket_name}' doesn't exist
    
            return False
################################################################################
    def download_file(self, info):
        bucket_name = info['bucket_name']
        object_name = info['object_name']

        s3_response = self.s3_client.list_buckets()
        list_of_buckets = [ bucket['Name'] for bucket in s3_response['Buckets'] ]
    
        if bucket_name in list_of_buckets:
            s3_response = self.s3_client.list_objects(Bucket=bucket_name)
            list_of_objects = [ key['Key'] for key in s3_response['Contents'] ]
    
            if object_name in list_of_objects:
#                logger.info(f"Retrieving the metadata of object '{object_name}' in bucket '{bucket_name}'")
                # Retrieve metadata from object in bucket
                metadata = self.s3_client.head_object(Bucket=bucket_name,Key=object_name)
    
#                logger.info(f"Downloading object '{object_name}' in bucket '{bucket_name}' with metadata '{metadata['Metadata']}'")
    
                fileobj = io.BytesIO()
                self.s3_client.download_fileobj(bucket_name, object_name, fileobj)
                fileobj.seek(0)
 
                res = {"bucket_name": bucket_name, "object_name": object_name,
                       "metadata": json.dumps(metadata['Metadata'])}
    
                return fileobj.read()
            else:
                return False
################################################################################
################################################################################
################################################################################
