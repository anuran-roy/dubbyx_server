from fastapi import FastAPI, UploadFile, APIRouter

# from fastapi import WebSocket, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
# from scripts.google_api import request_google_translate
# from scripts.indic_nlp import request_indicnlp_translate
from models.models import TranslatorData, Text2SpeechData

# import time
# import asyncio
import random

# from typing import Any
from pydantic import BaseModel
from io import BytesIO
# from pydub import AudioSegment
# from pydub.playback import play
# from playsound import playsound
from uuid import uuid4
import os
import detectlanguage
from ibm_watson.websocket import RecognizeCallback
from typing import Optional, List, Dict

# from ibm_watson.websocket import AudioSource
from ibm_watson import SpeechToTextV1, LanguageTranslatorV3, TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json


app = FastAPI(
    title="DubbyX backend", description="API Specifications for the DubbyX project"
)

detectlanguage.configuration.api_key = "8e5e3654fa4dc2e9742c5d3fdc3dfc6e"

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

translate_router: APIRouter = APIRouter(prefix="/translator", tags=["Translator APIs"])
s2t_router: APIRouter = APIRouter(prefix="/speech_to_text", tags=["Speech2Text APIs"])
t2s_router: APIRouter = APIRouter(prefix="/text_to_speech", tags=["Text2Speech APIs"])

############# API Config init

s2t_authenticator = IAMAuthenticator("MQu4YktchhGN5kLXKRUfozxeNdJRqtD3f_NrcBf0hAPE")
speech_to_text = SpeechToTextV1(authenticator=s2t_authenticator)
speech_to_text.set_service_url(
    "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/3c1a6152-5cfc-4b67-80d1-7b187b15d127"
)


translator_authenticator = IAMAuthenticator(
    "CEGbKRAcuBkM-LYUD3denZzSLIo8Js6nZUDlOskaFxmJ"
)
language_translator = LanguageTranslatorV3(
    version="2018-05-01", authenticator=translator_authenticator
)

language_translator.set_service_url(
    "https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/8658739a-b2dc-4a17-966d-a24f7589c949"
)


t2s_authenticator = IAMAuthenticator("M98yrQWuU_7hRn6Wwil9nQwwjb_d8qRdnHFsYFrtoET0")
text_to_speech = TextToSpeechV1(authenticator=t2s_authenticator)

text_to_speech.set_service_url(
    "https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/e207bf9c-06ab-45f6-b51e-62762dd93382"
)

#############


class FileUpload(BaseModel):
    fileUpload: str


# class DummyGenerator:
#     def __iter__(self):
#         return self
#     def __next__(self):
#         return random.randint(0,10000)


def dummyNumber():
    return random.randint(0, 10000)


# @app.websocket("/translate/google")
# async def google_transcribe(ws: WebSocket):
#     # obj = DummyGenerator()
#     await ws.accept()

#     while (await ws.receive())["text"] == "start_feed":
#         print("WebSocket data received")
#         printable = dummyNumber()
#         print(printable)
#         await ws.send_text(f"{printable}")
#     print("WebSocket CLOSING")
#     await ws.close()


class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print("Error received: {}".format(error))

    def on_inactivity_timeout(self, error):
        print("Inactivity timeout: {}".format(error))


# myRecognizeCallback = MyRecognizeCallback()

# with open(join(dirname(__file__), './.', 'audio-file.flac'),
#               'rb') as audio_file:
#     audio_source = AudioSource(audio_file)
#     speech_to_text.recognize_using_websocket(
#         audio=audio_source,
#         content_type='audio/flac',
#         recognize_callback=myRecognizeCallback,
#         model='en-US_BroadbandModel',
#         keywords=['colorado', 'tornado', 'tornadoes'],
#         keywords_threshold=0.5,
#         max_alternatives=3)


@translate_router.post("/transcribe/google")
# def google_transcribe(fileUpload: UploadFile):
#     print("Data received!")
#     print(fileUpload.__dict__)

#     in_memory_file = BytesIO(fileUpload.file.read())

#     client = speech.SpeechClient()

#     folder_name = uuid4().hex
#     if not os.path.exists(f"./uploads/{folder_name}"):
#         os.makedirs(f"./uploads/{folder_name}")

#     with open(f"./uploads/{folder_name}/{fileUpload.filename}", "wb") as out_file:
#         content = in_memory_file.read()
#         out_file.write(content)

#     detectlanguage.simple_detect("")

#     # myRecognizeCallback = MyRecognizeCallback()

#     # # song = AudioSegment.from_file("hello.wav", format="wav")
#     # # play(song)
#     # # playsound("./hello.wav")

#     # stream = [content]

#     # requests = (
#     #     speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream
#     # )

#     # config = speech.RecognitionConfig(
#     #     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     #     sample_rate_hertz=48000,
#     #     language_code="en-US",
#     # )

#     # streaming_config = speech.StreamingRecognitionConfig(config=config)

#     # # streaming_recognize returns a generator.
#     # responses = client.streaming_recognize(
#     #     config=streaming_config,
#     #     requests=requests,
#     # )

#     # for response in responses:
#     #     # Once the transcription has settled, the first result will contain the
#     #     # is_final result. The other results will be for subsequent portions of
#     #     # the audio.
#     #     for result in response.results:
#     #         print(f"Finished: {result.is_final}")
#     #         print(f"Stability: {result.stability}")
#     #         alternatives = result.alternatives
#     #         # The alternatives are ordered from most likely to least.
#     #         for alternative in alternatives:
#     #             print(f"Confidence: {alternative.confidence}")
#     #             print(f"Transcript: {alternative.transcript}")

#     responses = {}
#     return {"message": "File received!", "responses": responses}


# @translate_router.post("/indicnlp")
# async def indicnlp_translate(fileUpload: UploadFile):
#     print("Data received!")
#     print(fileUpload.__dict__)

#     in_memory_file = BytesIO(fileUpload.file.read())

#     with open(f"./uploads/{fileUpload.filename}", "wb") as out_file:
#         out_file.write(in_memory_file.read())
#     # song = AudioSegment.from_file("hello.wav", format="wav")
#     # play(song)
#     # playsound("./hello.wav")
#     return {"message": "File received!"}


@translate_router.post("/watson")
def watson_translate(data: TranslatorData):
    """Translate the given data using IBM Watson."""
    translation = language_translator.translate(
        text=data.text, model_id=f"{data.source_lang}-{data.target_lang}"
    ).get_result()

    # print(json.dumps(translation, indent=2, ensure_ascii=False))
    return translation


@t2s_router.post("/watson", response_class=FileResponse)
def watson_t2s(data: Text2SpeechData):
    """Gets translated data from IBM Watson Translate and uploads a file to a cloud bucket."""

    content = BytesIO()

    voice_dict: Dict[Dict[str, List[str]]] = {
        "ar": {"MS": {"m": ["ar-MS_OmarVoice"]}},
        "cs": {
            "CZ": {
                "f": ["cs-CZ_AlenaVoice"],
            }
        },
        "de": {
            "DE": {
                "m": ["de-DE_BirgitV3Voice", "de-DE_DieterV3Voice"],
                "f": ["de-DE_ErikaV3Voice"],
            }
        },
        "en": {
            "AU": {
                "m": ["en-AU_CraigVoice", "en-AU_SteveVoice"],
                "f": ["en-AU_MadisonVoice"],
            },
            "GB": {
                "f": ["en-GB_CharlotteV3Voice", "en-GB_KateV3Voice"],
                "m": ["en-GB_JamesV3Voice"],
            },
            "US": {
                "f": [
                    "en-US_AllisonExpressive",
                    "en-US_AllisonV3Voice",
                    "en-US_EmilyV3Voice",
                    "en-US_EmmaExpressive",
                    "en-US_OliviaV3Voice",
                    "en-US_LisaExpressive",
                    "en-US_LisaV3Voice",
                ],
                "m": [
                    "en-US_HenryV3Voice",
                    "en-US_KevinV3Voice",
                    "en-US_MichaelExpressive",
                    "en-US_MichaelV3Voice",
                ],
            },
        },
        "es": {
            "ES": {
                "m": [
                    "es-ES_EnriqueV3Voice",
                ],
                "f": [
                    "es-ES_LauraV3Voice",
                ],
            },
            "LA": {
                "f": ["es-LA_SofiaV3Voice"],
            },
            "US": {"f": ["es-US_SofiaV3Voice"]},
        },
        "fr": {
            "CA": {"f": ["fr-CA_LouiseV3Voice"]},
            "FR": {
                "m": ["fr-FR_NicolasV3Voice"],
                "f": ["fr-FR_ReneeV3Voice"],
            },
        },
        "it-IT": {
            "f": ["it-IT_FrancescaV3Voice"],
        },
        "ja": {
            "JP": {
                "f": ["ja-JP_EmiV3Voice"],
            }
        },
        "ko": {
            "KR": {
                "m": ["ko-KR_HyunjunVoice", "ko-KR_SiWooVoice"],
                "f": ["ko-KR_YoungmiVoice", "ko-KR_YunaVoice"],
            }
        },
        "nl": {
            "BE": {
                "m": ["nl-BE_AdeleVoice"],
                "f": ["nl-BE_BramVoice"],
            },
            "NL": {
                "m": ["nl-NL_EmmaVoice"],
                "f": ["nl-NL_LiamVoice"],
            },
        },
        "pt": {
            "BR": {
                "f": ["pt-BR_IsabelaV3Voice"],
            }
        },
        "sv": {
            "SE": {
                "m": ["sv-SE_IngridVoice"],
            }
        },
        "zh": {
            "CN": {
                "m": ["zh-CN_LiNaVoice"],
                "f": ["zh-CN_WangWeiVoice", "zh-CN_ZhangJingVoice"],
            }
        },
    }

    lang: str = data.source_lang
    acnt: str = data.accent
    gender: str = data.voice

    for language in voice_dict.keys():
        if lang == language:
            if acnt not in voice_dict[language]:
                 acnt = voice_dict[language].keys()[0]
                 if gender not in voice_dict[language][acnt]:
                     gender = voice_dict[language][acnt].keys()[0]
    
    print(voice_dict[lang][acnt][gender])
    res_content = text_to_speech.synthesize(
        data.text,
        voice=voice_dict[lang][acnt][gender][0],
        accept="audio/wav",
    ).get_result().content
    # content.write()
    
    print(res_content)
    return BytesIO(res_content)


# @t2s_router.post("/google")
# def google_t2s(data: Text2SpeechData):
#     """Gets translated data from Google Translate and uploads a file to the bucket."""

#     # The ID of your GCS bucket
#     bucket_name = "wearable-project"

#     # The contents to upload to the file
#     contents = BytesIO()

#     # The ID of your GCS object
#     destination_blob_name = "storage-object-name"

#     storage_client = storage.Client()
#     bucket = storage_client.bucket(bucket_name)
#     blob = bucket.blob(destination_blob_name)

#     blob.upload_from_string(contents)

#     print(
#         f"{destination_blob_name} with contents {contents} uploaded to {bucket_name}."
#     )


app.include_router(translate_router)
app.include_router(s2t_router)
app.include_router(t2s_router)
