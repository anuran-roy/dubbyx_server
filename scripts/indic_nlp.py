import requests
from io import BytesIO


async def request_indicnlp_translate(data: BytesIO):
    return {"translation": "Hello, world!"}
