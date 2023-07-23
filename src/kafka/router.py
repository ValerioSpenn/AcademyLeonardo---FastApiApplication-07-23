from fastapi import APIRouter
from models.KafkaMessage import TssVitals, KafkaMessage, Position, DateObserved, TypeMessage, Payload, ImageId
import random
import uuid

router = APIRouter()

@router.post("/send_tss_vitals", tags=["Send TSS Vitals"], description="Endpoint to send tss vitals on kafka got from AI Model")
async def create_tss_vitals_message(tss_vitals: TssVitals, _position_value: Position, _image_name_value: str) -> KafkaMessage:
    random_heart_rate = random.randint(60, 100)
    random_respiratory_rate = random.randint(12, 20)
    random_skin_temperature = round(random.uniform(35.0, 37.5), 2)
    random_victim_id = str(uuid.uuid4())
    random_image_name = "image_" + str(random.randint(1, 100))
    random_bucket_name = "bucket_" + str(random.randint(1, 10))
    random_base_url = "http://example.com/images"
    random_lat = round(random.uniform(-90, 90), 6)
    random_long = round(random.uniform(-180, 180), 6)
    random_alt = round(random.uniform(0, 500), 2)
    random_timestamp = "2023-07-23T12:34:56Z"

    image_id = ImageId(image_name=random_image_name, bucket_name=random_bucket_name, base_url=random_base_url)
    position = Position(lat=random_lat, long=random_long, alt=random_alt)
    date_observed = DateObserved(value=random_timestamp)
    payload = Payload(
        victim_id=random_victim_id,
        heart_rate=random_heart_rate,
        respiratory_rate=random_respiratory_rate,
        skin_temperature=random_skin_temperature,
        image_id=image_id,
        position=position,
        timestamp=random_timestamp
    )

    random_type = random.choice(list(TypeMessage))

    kafka_message = KafkaMessage(id=1, type=random_type, dateObserved=date_observed, payload=payload)

    return kafka_message
