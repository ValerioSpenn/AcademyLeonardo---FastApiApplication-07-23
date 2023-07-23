from fastapi import APIRouter

router = APIRouter()#title= "Hello World API")

@router.get("/hello_world", tags=["Hello World"], description="Endpoint per ottenere il messaggio di saluto")
async def get_posts():
    return{'Hello World'}
