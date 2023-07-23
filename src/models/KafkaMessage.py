from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
import random
import uuid

class DateObserved(BaseModel):
    type: str = "DateTime"
    value: str

class ImageId(BaseModel):
    image_name: str
    bucket_name: str
    base_url: str

class Position(BaseModel):
    lat: float
    long: float
    alt: float

class TssVitals(BaseModel):
    heart_rate: int = Field(..., ge=0, le=200)
    respiratory_rate: int = Field(..., ge=0, le=40)
    skin_temperature: float = Field(..., ge=0, le=50)


class Payload(BaseModel):
    victim_id: str
    heart_rate: int = Field(..., ge=0, le=200)
    respiratory_rate: int = Field(..., ge=0, le=40)
    skin_temperature: float = Field(..., ge=0, le=50)
    image_id: ImageId
    position: Position
    timestamp: str

class TypeMessage(str, Enum):
    Type1 = "Type1"
    Type2 = "Type2"
    Type3 = "Type3"

class KafkaMessage(BaseModel):
    id: int
    type: TypeMessage
    dateObserved: DateObserved
    payload: Payload

    @classmethod
    def MessageSimulation(cls):
        datetimeNOW = datetime.now()
        message = cls(
            id=random.randint(1000, 2000),
            type=random.choice([TypeMessage.Type1, TypeMessage.Type2, TypeMessage.Type3]),
            dateObserved=DateObserved(value=datetimeNOW.strftime("%T-%m-%dT%H:%M:%S.%f%z")),
            payload=Payload(
                victim_id=str(uuid.uuid4()),
                heart_rate=random.randint(60, 100),
                respiratory_rate=random.randint(12, 16),
                skin_temperature=round(random.uniform(36.5, 37.2), 1),
                image_id=ImageId(
                    image_name="vitals_victim_0.JPG",
                    bucket_name="tss-bucket-test",
                    base_url="http://nightingale.minio/tss/"
                ),
                position=Position(
                    lat=round(random.uniform(-90, 90), 5),
                    long=round(random.uniform(-180, 180), 5),
                    alt=round(random.uniform(-1000, 1000), 5)
                ),
                timestamp=datetimeNOW.strftime("%T-%m-%dT%H:%M:%S.%f%z")
            )
        )
        return message


