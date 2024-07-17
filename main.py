from io import BytesIO

from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import numpy as np
import cv2
from zep_python import ZepClient
import os
from imgbeddings import imgbeddings
import uvicorn
from zep_python.document import Document

app = FastAPI()

zep_url = os.getenv("ZEP_URL", "http://localhost:8000")
client = ZepClient(zep_url)
collection_name = "recognitionfaces"
collection = None

try:
    collection = client.document.get_collection(collection_name)
except Exception as e:
    collection = client.document.add_collection(
        name=collection_name,
        description="Face Recognition Engine",
        embedding_dimensions=768,
        is_auto_embedded=False,
    )


class ImageData(BaseModel):
    name: str
    image: UploadFile


class RecognizeResponse(BaseModel):
    name: str
    confidence: float


async def get_face_from_photo(image):
    alg = "haarcascade_frontalface_default.xml"
    haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + alg)
    image_bytes = await image.read()
    image_np = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    faces = haar_cascade.detectMultiScale(img, scaleFactor=1.05, minNeighbors=2, minSize=(100, 100))
    if len(faces) == 0:
        raise HTTPException(status_code=400, detail="No face found in the image")
    x, y, w, h = faces[0]
    cropped_image = img[y: y + h, x: x + w]

    _, buffer = cv2.imencode('.jpg', cropped_image)
    image_bytes = buffer.tobytes()
    image_stream = BytesIO(image_bytes)

    return Image.open(image_stream)


@app.post("/add-image")
async def add_image(name: str, image: UploadFile = File(...)):
    global client
    try:
        cropped_image = await get_face_from_photo(image)
        ibed = imgbeddings()
        embedding = ibed.to_embeddings(cropped_image)[0]
        emb_array = np.array(embedding).reshape(1, -1)
        embedding_list = emb_array.tolist()

        collection.add_documents([
            Document(content=name, embedding=embedding_list[0])
        ])

        return {"status": "success", "name": name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/recognize", response_model=RecognizeResponse)
async def recognize(image: UploadFile = File(...)):
    global client
    try:
        cropped_image = await get_face_from_photo(image)
        ibed = imgbeddings()
        embedding = ibed.to_embeddings(cropped_image)[0]
        emb_array = np.array(embedding).reshape(1, -1)
        embedding_list = emb_array.tolist()
        result = collection.search(embedding=embedding_list[0], limit=5)

        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Face not recognized")

        best_match = result[0]

        return RecognizeResponse(name=best_match.content, confidence=best_match.score)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=18000)
