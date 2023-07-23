from fastapi import FastAPI
import uvicorn
from posts.router import router as posts_router
from kafka.router import router as kafka_router
from minio.router import router as minio_router


app = FastAPI()

app.include_router(posts_router)
app.include_router(kafka_router)
app.include_router(minio_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
