import requests
from io import BytesIO


async def request_google_translate(data: BytesIO):
    return {"translation": "Hello, world!"}
