# main.py

from fastapi import FastAPI
import makenoise as mn
import torch
import urllib.request
from PIL import Image
from transformers import EfficientNetImageProcessor, EfficientNetForImageClassification
preprocessor = EfficientNetImageProcessor.from_pretrained("dennisjooo/Birds-Classifier-EfficientNetB2")
bird_classification_model = EfficientNetForImageClassification.from_pretrained("dennisjooo/Birds-Classifier-EfficientNetB2")


app = FastAPI()
async def classify_bird(img):
    inputs = preprocessor(img, return_tensors="pt")
    # Running the inference
    with torch.no_grad():
        logits = model(**inputs).logits
    
    # Getting the predicted label
    predicted_label = logits.argmax(-1).item()
    print(model.config.id2label[predicted_label])
    
@app.get("/bark/{sound_file}")
async def bark(sound_file: str ):
    sound_files = ['mixkit-dog-barking-twice-1.wav','mixkit-giant-dog-aggressive-growl-59.wav', 'mixkit-hellhound-monster-attack-dog-wolf-creature-3015.wav']  
    await mn.dog_bark(sound_file)
    return (f'Barking 1: {sound_file}')

@app.get("/bird/{bird_image}")
async def identify_bird(bird_image):
    bird_type = await classify_bird(bird_image)
    return bird_type
    