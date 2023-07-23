from pydantic import BaseModel

class AWSClient(BaseModel):
    endpoint_url: str
    aws_access_key_id: str
    aws_secret_access_key: str
    signature_version: str